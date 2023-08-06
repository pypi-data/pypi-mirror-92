import logging

_LEVELS = {
    'all': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR,
}


def configure_arg_parser_for_log(args_parser) -> None:
    args_parser.add_argument('-l', '--log', help='Log level', default='debug', choices=['all', 'debug', 'info', 'warn', 'error', 'none'])


def configure_logger(env) -> None:
    assert env.log, env

    msg_fmt = '%(levelname)s %(asctime)s [%(name)s] %(message)s'

    if env.log == 'none':
        logging.disable(logging.CRITICAL)
    else:
        lev = _LEVELS.get(env.log, None)
        if lev is None:
            raise SystemExit('Invalid value for logging level: "{}". Use all,debug,info,warn,error.'.format(env.log))
        #logging.basicConfig(level=lev, format=msg_fmt)

    logging.addLevelName(logging.CRITICAL, '!!!')
    logging.addLevelName(logging.ERROR, '!! ')
    logging.addLevelName(logging.WARNING, '!  ')
    logging.addLevelName(logging.INFO, '   ')
    logging.addLevelName(logging.DEBUG, '   ')

    root_log = logging.getLogger()
    root_log.setLevel(logging.DEBUG)    
    
    fh = logging.FileHandler('root.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(msg_fmt))
    
    cons = logging.StreamHandler()
    cons.setLevel(logging.INFO)
    cons.setFormatter(logging.Formatter(msg_fmt))
   
    root_log.addHandler(cons)
    root_log.addHandler(fh)
