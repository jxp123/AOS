
def validate_equipment_compatibility(source_equipment, target_equipment):
    if not source_equipment or not target_equipment:
        return False, 'Unknown equipment type'
    if source_equipment == 'Unknown' or target_equipment == 'Unknown':
        return False, 'Unknown equipment type'
    if source_equipment != target_equipment:
        return False, f'Incompatible equipment: {source_equipment} -> {target_equipment}'
    return True, 'Compatible'

def validate_national_donor(colony):
    if colony.get('equipment') != 'National':
        return False, f"{colony.get('code')} is {colony.get('equipment')}, not National"
    return True, 'National donor validated'
