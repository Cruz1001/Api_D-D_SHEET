from app.schemas.character import Skill, CharacterBase

ALL_SKILLS = [
    {"name": "Athletics", "attribute": "strength"},
    {"name": "Acrobatics", "attribute": "dexterity"},
    {"name": "Sleight of Hand", "attribute": "dexterity"},
    {"name": "Stealth", "attribute": "dexterity"},
    {"name": "Arcana", "attribute": "intelligence"},
    {"name": "History", "attribute": "intelligence"},
    {"name": "Investigation", "attribute": "intelligence"},
    {"name": "Nature", "attribute": "intelligence"},
    {"name": "Religion", "attribute": "intelligence"},
    {"name": "Animal Handling", "attribute": "wisdom"},
    {"name": "Insight", "attribute": "wisdom"},
    {"name": "Medicine", "attribute": "wisdom"},
    {"name": "Perception", "attribute": "wisdom"},
    {"name": "Survival", "attribute": "wisdom"},
    {"name": "Deception", "attribute": "charisma"},
    {"name": "Intimidation", "attribute": "charisma"},
    {"name": "Performance", "attribute": "charisma"},
    {"name": "Persuasion", "attribute": "charisma"},
]
# --- ADICIONE ISSO AQUI ---
ALL_SAVES = [
    {"name": "Strength", "attribute": "strength"},
    {"name": "Dexterity", "attribute": "dexterity"},
    {"name": "Constitution", "attribute": "constitution"},
    {"name": "Intelligence", "attribute": "intelligence"},
    {"name": "Wisdom", "attribute": "wisdom"},
    {"name": "Charisma", "attribute": "charisma"},
]

def attribute_modifier(score: int) -> int:
    return (score - 10) // 2

def generate_skills(character: CharacterBase) -> list[Skill]:
    return [
        Skill(
            name=skill["name"],
            attribute=skill["attribute"],
            proficient=False,
            value=attribute_modifier(getattr(character, skill["attribute"]))
        )
        for skill in ALL_SKILLS if skill # o if skill evita o erro do dicionário vazio {} que estava no seu código
    ]

# --- ADICIONE ESSA FUNÇÃO TAMBÉM ---
def generate_saving_throws(character: CharacterBase) -> list[Skill]:
    return [
        Skill(
            name=save["name"],
            attribute=save["attribute"],
            proficient=False,
            value=attribute_modifier(getattr(character, save["attribute"]))
        )
        for save in ALL_SAVES
    ]