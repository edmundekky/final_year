# matcher.py
from profiler.models import (
    Alias,
    AssociatedDevice,
    AssociatedIP,
    CyberCriminal,
    Technique,
)


# Define weights for each attribute
WEIGHTS = {
    "ip": 5,
    "alias": 4,
    "technique": 3,
    "device": 2,
    "tactic": 1,
}


def get_best_by_technique(criminals, temp_criminal):
    # find the most similar criminals based on the number of similar techniques used
    similar_criminals = []
    for criminal in criminals:
        similar_techniques = len(
            set(temp_criminal.techniques.all()) & set(criminal.techniques.all())
        )
        if similar_techniques > 0:
            similar_criminals.append((criminal, similar_techniques))

    #  make sure the temp_criminal is not in the list of similar criminals
    return sorted(similar_criminals, key=lambda x: x[1], reverse=True)


def get_best_by_tactic(criminals, temp_criminal):
    # find the most similar criminals based on the number of similar tactics used
    similar_criminals = []
    for criminal in criminals:
        similar_tactics = len(
            set(temp_criminal.tactics.all()) & set(criminal.tactics.all())
        )
        if similar_tactics > 0:
            similar_criminals.append((criminal, similar_tactics))

    return sorted(similar_criminals, key=lambda x: x[1], reverse=True)


def get_best_by_alias(criminals, temp_criminal):
    temp_aliases = []
    similar_criminals = []

    for alias in temp_criminal.aliases.all():
        temp_aliases.append(f"{alias.name}")

    for criminal in criminals:
        similar_aliases = len(
            set(temp_aliases) & set([alias.name for alias in criminal.aliases.all()])
        )
        if similar_aliases > 0:
            similar_criminals.append((criminal, similar_aliases))

    return sorted(similar_criminals, key=lambda x: x[1], reverse=True)


def get_best_by_ip(criminals, temp_criminal):
    temp_ips = []
    similar_criminals = []

    for ip in temp_criminal.associated_ips.all():
        temp_ips.append(ip.ip_address)

    for criminal in criminals:
        similar_ips = len(
            set(temp_ips) & set([ip.ip_address for ip in criminal.associated_ips.all()])
        )
        if similar_ips > 0:
            similar_criminals.append((criminal, similar_ips))

    return sorted(similar_criminals, key=lambda x: x[1], reverse=True)


def get_best_by_device(criminals, temp_criminal):
    temp_devices = []
    similar_criminals = []

    for device in temp_criminal.associated_devices.all():
        temp_devices.append(f"{device.device_name}")

    for criminal in criminals:
        similar_devices = len(
            set(temp_devices)
            & set([device.device_name for device in criminal.associated_devices.all()])
        )
        if similar_devices > 0:
            similar_criminals.append((criminal, similar_devices))

    return sorted(similar_criminals, key=lambda x: x[1], reverse=True)


def match_criminal(temp_criminal):
    # get the criminals except for the temp_criminal
    criminals = CyberCriminal.objects.exclude(id=temp_criminal.id)

    similar_by_technique = get_best_by_technique(criminals, temp_criminal)
    similar_by_alias = get_best_by_alias(criminals, temp_criminal)
    similar_by_device = get_best_by_device(criminals, temp_criminal)
    similar_by_tactic = get_best_by_tactic(criminals, temp_criminal)
    similar_by_ip = get_best_by_ip(criminals, temp_criminal)

    # Calculate total weighted matches for each criminal
    total_matches = {}
    for criminal_list, attribute in zip(
        [
            similar_by_ip,
            similar_by_alias,
            similar_by_device,
            similar_by_technique,
            similar_by_tactic,
        ],
        ["ip", "alias", "device", "technique", "tactic"],
    ):
        for criminal, matches in criminal_list:
            if criminal in total_matches:
                total_matches[criminal] += WEIGHTS[attribute] * matches
            else:
                total_matches[criminal] = WEIGHTS[attribute] * matches

    # Sort criminals by total number of matches
    sorted_criminals = sorted(total_matches.items(), key=lambda x: x[1], reverse=True)

    if not sorted_criminals:
        return None
    elif len(sorted_criminals) > 3:
        return sorted_criminals[:3]
    else:
        return sorted_criminals


def match_projected_techniques(temp_criminal, matched_criminals):
    # create a set of all the total matched techniques in the matched_criminals and the temp_criminal
    all_techniques = set()
    projected_techniques = []

    all_techniques.update(temp_criminal.techniques.all())

    for criminal, _ in matched_criminals:
        all_techniques.update(criminal.techniques.all())

    for technique in all_techniques:
        if technique not in temp_criminal.techniques.all():
            projected_techniques.append(technique)

    # sort the techniques by the number of criminals that use them
    possible_techniques = sorted(
        projected_techniques,
        key=lambda x: len(
            [
                criminal
                for criminal, _ in matched_criminals
                if technique in criminal.techniques.all()
            ]
        ),
        reverse=True,
    )
    return possible_techniques
