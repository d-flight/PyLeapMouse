import sys

if sys.platform == "darwin":
    import MacOS.Leap as Leap
    import MacOS.Mouse as Mouse
elif 'linux' in sys.platform:
    import Linux.Leap as Leap
    import Linux.Mouse as Mouse
else:
    print "Only macOS & Linux are supported."
    exit(1)
