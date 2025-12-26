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


def attribute_modifier(score: int) -> int:
    return (score - 10) // 2


def generate_skills(character: CharacterBase) -> list[Skill]:
    return [
        Skill(
            name=skill["name"],
            attribute=skill["attribute"],
            proficient=False,
            value=attribute_modifier(
                getattr(character, skill["attribute"])
            )
        )
        for skill in ALL_SKILLS
    ]
