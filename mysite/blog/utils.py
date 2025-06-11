def build_tree(root_member):
    """Рекурсивное построение дерева семьи"""
    tree = {
        'member': root_member,
        'children': []
    }
    
    # Добавляем детей
    for child in root_member.children.all():
        tree['children'].append(build_tree(child))
    
    return tree