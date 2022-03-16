from definitions import DAYS

def print_to_console(fixed, flex, msol):
    if msol:
        print("Solution:")
        print(" Fixed:")
        for s in sorted(fixed,key=lambda s:msol[s]):
            print("  " + str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))
        print(" Flex:")
        for s in sorted(flex,key=lambda s:msol[s]):
            print("  " + str(msol[s]) + "  -> " + DAYS[msol[s]//24] + " kl. " + str(msol[s]%24))
        print()
    else:
        print("Solve status: " + msol.get_solve_status())