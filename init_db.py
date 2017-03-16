from lib.initialization.init_database import main_init
import time

try:
    start = time.time()
    main_init()
    end = time.time()
    print "Success init Database took %g s" % (end - start)

except:
    print "errors"