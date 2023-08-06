from enum import Enum
from collections import namedtuple

from .ocpp15.base import *
from .ocpp15.types import *
from .time_tools import Timeout
from .ocpp_payload_reader import MsgReader

class ChargerState(Enum):
    Offline = 0     # also when rejected from boot notification
    WaitBootNotificationResponse = 1
    Accepted = 2


ChargerInfo = namedtuple('ChargerInfo', 'Id CentralStationAddress ChargerPublicAddress NbConnectors Meta CloudInfo')


class Charger:
    def __init__(self, charger_info):
        self.Info = charger_info
        self._state = ChargerState.Offline
        self._timeout = Timeout(0, expired=True)    # Запрещает любые новые запросы
        self._log = logging.getLogger()
    
        # List of tuples (action, payload, cb)
        self._req_queue = []
        self._heartbeat_timeout = None
    
    def _pend_request(self, action, payload, cb):
        self._req_queue.append((action, payload, cb))

    # Returns Payload or throw OcppError
    def on_request_from_cs(self, action: str, payload: dict) -> dict:
        return self._process_payload(self._respond(action, payload))
            
    def _respond(self, action: str, payload: dict) -> dict:
        log = self._log
        
        reader = MsgReader(action, payload, self.Info, log)
        # Reset
        if action == 'Reset':
            return {'status': ResetStatus.Accepted}
        
        # ChangeConfiguration
        elif action == 'ChangeConfiguration':
            k = reader.str('key')
        
            if k=='HeartBeatInterval':
                v = reader.int('value')
                log.info(f'Set Heartbeat to {v} sec')
                self._heartbeat_timeout = Timeout(v)
            else:
                v = reader.str('value')
                log.info(f'Set {k}={v}')
            
            return {'status': ConfigurationStatus.Accepted}
        
        # ChangeAvailability
        elif action == 'ChangeAvailability':
            # The id of the connector for which availability needs to change. Id '0' (zero) is used if the availability of the charge point as a whole needs to change.
            connectorId = reader.int('connectorId')
            type = reader.enum('type', AvailabilityType)
            
            return {'status': AvailabilityStatus.Accepted}
        
        # RemoteStartTransaction
        elif action == 'RemoteStartTransaction':
            connectorId = reader.int('connectorId', -1)
            idTag = reader.str('idTag', MaxLen.IdToken)
            
            return self._process_payload({'status': RemoteStartStopStatus.Accepted})
        
        # RemoteStopTransaction
        elif action == 'RemoteStopTransaction':
            transactionId = reader.int('transactionId')
            
            return self._process_payload({'status': RemoteStartStopStatus.Accepted})
        
        # ReserveNow
        elif action == 'ReserveNow':
            # [integer] Mandatory. This contains the id of the connector to be reserved. A value of 0 means that the reservation is not for a specific connector.
            connectorId = reader.int('connectorId')
            # [dateTime] Mandatory. This contains the date and time when the reservation ends.
            expiryDate = reader.dtm('expiryDate')
            # [IdToken] Mandatory. The identifier for which the Charge Box has to reserve a connector.
            idTag = reader.str('idTag', MaxLen.IdToken)
            # [IdToken] Optional. The parent id-tag.
            parentIdTag = reader.str('parentIdTag', MaxLen.IdToken, 0)
            # [integer] Mandatory. Unique id for this reservation.
            reservationId = reader.int('reservationId')
            
            return {'status': ReservationStatus.Accepted}
        
        # CancelReservation
        elif action == 'CancelReservation':
            reservationId = reader.int('reservationId')
            
            return {'status': CancelReservationStatus.Accepted}
        else:
            raise OcppError(f'Action {action} is not supported', OcppErrorCode.NotSupported)
            
    # (Action, Payload, Callback|None) or None
    def get_request_to_cs(self) -> tuple:    
        log = self._log

        if not self._timeout.is_expired():
            return None
            
        s = self._state
        
        if s == ChargerState.Offline:
            self._state = ChargerState.WaitBootNotificationResponse
            return ('BootNotification', self._boot_notification_payload(), self.cb_BootNotification)

        elif s == ChargerState.WaitBootNotificationResponse:
            return None

        elif s == ChargerState.Accepted:
            if self._heartbeat_timeout.is_expired():
                self._heartbeat_timeout.start()
                return ('Heartbeat', {}, None)
                
            return self._req_queue.pop(0) if self._req_queue else None
            
        else:
            raise Exception(f'Unknown charger state: {self._state}')
        
    def cb_BootNotification(self, resp_payload: (dict, None)):
        assert resp_payload is None or isinstance(resp_payload, dict), resp_payload
        log = self._log
        
        #if self._state != ChargerState.WaitBootNotificationResponse:
        #    raise Exception(f'Received BootNotification response in {self._state} state')

        if resp_payload is None:
            self._offline('Failed boot notification')
            return

        reader = MsgReader(None, resp_payload, self.Info, log)

        status = reader.enum('status', RegistrationStatus)
            
        if status == RegistrationStatus.Accepted:
            currentTime = reader.dtm('currentTime')
            heartbeatInterval = reader.int('heartbeatInterval')
            
            log.info(f'Set Heartbeat to {heartbeatInterval} sec')
            self._heartbeat_timeout = Timeout(heartbeatInterval)
            
            self._state = ChargerState.Accepted
            for i in range(self.Info.NbConnectors):
                payload = {
                    'connectorId': i + 1,
                    'status': 'Available',
                    'errorCode': 'NoError',
                    'timestamp': utc_str(),
                }
                self._pend_request('StatusNotification', payload, None)

        else:
            self._offline(f'Charger rejected on cs: {resp_payload}. Device moved to Offline')
        
    def _boot_notification_payload(self) -> dict:
        msg_def = BootNotificationReq
        payload = {}
    
        for field_name, is_optional in msg_def:
            if field_name in self.Info.Meta:
                payload[field_name] = self.Info.Meta[field_name]
            elif not is_optional:
                raise Exception(f'Field "{field_name}" is required, but missing in charger {self.Info}')
        
        return payload
    
    def _offline(self, msg, timeout = 5.0):
        self._log.error(msg)
        self._state = ChargerState.Offline
        self._timeout.start(timeout)
        self._req_queue = []
    
    def manual_Authorize(self, tag: str):
        pld = {
            'idTag':    tag
        }
        self._pend_request('Authorize', pld, None)
    
    def _process_payload(self, payload: dict) -> dict:
        """
            Заменяет в иерархическом JSON объекте все Enum на их строковые значения
        """
        for k, v in payload.items():
            if isinstance(v, Enum):
                payload[k] = v.value
            elif isinstance(v, dict):
                process_payload(v)
        return payload