import pexpect, sys

__all__ = [ 'expect_gdb', 'send_gdb','expect_rr', 'send_rr', 'ok' ]

# Public API
def expect_gdb(what):
    expect(gdb, what)

def expect_rr(what):
    expect(rr, what)

def send_gdb(what):
    send(gdb, what)

def send_rr(what):
    send(rr, what)

def ok():
    clean_up()

# Internal helpers
TIMEOUT_SEC = 5
gdb = None
rr = None

def clean_up():
    global gdb, rr
    if gdb:
        gdb.close(force=1)
        gdb = None
    if rr:
        rr.close(force=1)
        rr = None

def expect(prog, what):
    try:
        prog.expect(what)
    except Exception, e:
        failed('expecting "%s"'% (what), e)

def failed(why, e):
    print 'FAILED:', why
    if e:
        print 'exception:', e
    clean_up()
    sys.exit(1)

def get_rr_cmd():
    '''Return the command that should be used to invoke rr, as the tuple
  (executable, array-of-args)'''
    rrargs = sys.argv[1:]
    return (rrargs[0], rrargs[1:])

def send(prog, what):
    try:
        prog.send(what)
    except Exception, e:
        failed('sending "%s"'% (what), e)

def set_up():
    global gdb, rr
    try:
        rr = pexpect.spawn(*get_rr_cmd(), timeout=TIMEOUT_SEC, logfile=open('rr.log', 'w'))
        gdb = pexpect.spawn('gdb a.out', timeout=TIMEOUT_SEC, logfile=open('gdb.log', 'w'))

        expect_gdb('(gdb)')
        send_gdb('target remote :1111\n')
        expect_gdb('(gdb)')
    except Exception, e:
        failed('initializing rr and gdb', e)

set_up()
