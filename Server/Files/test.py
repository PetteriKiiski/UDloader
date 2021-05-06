import pickle
import contextlib
import gzip
try:
	with contextlib.closing(gzip.open('car_registrations.dat', "wb")) as fh:
		pickle.dump([], fh)
except (EnvironmentError, pickle.UnpicklingError) as err:
	print("server cannot load data: {0}".format(err))
	sys.exit(1)

