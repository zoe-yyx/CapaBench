def has_admitted(action):
    if "Admitted" in action:
        return True
    return False

def qed(results, proposition):
    for result in results:
        if "No more goals." in result and f"Stderr: {proposition} <" in result:
            return True
    return False


def has_error(results, proposition):
    for result in results:
        if "Error:" in result:
            return True
    return False

