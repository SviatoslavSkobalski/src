from common import archetypeNames

class Warrior:
	name = archetypeNames[0]
	strenghtIncrease = 3
	agilityIncrease = 7
	intelligenceIncrease = 1
	mainAttribute = 'strenght'
	damageModifier = 20
	skills = ['go berserk', 'mighty punch', 'blow a head off']

class Shaman:
	name = archetypeNames[1]
	strenghtIncrease = 1
	agilityIncrease = 3
	intelligenceIncrease = 7
	mainAttribute = 'intelligence'
	damageModifier = 10
	skills = ['nature heal', 'fire ball', 'hell from the sky']

class Trickster:
	name = archetypeNames[2]
	strenghtIncrease = 1
	agilityIncrease = 7
	intelligenceIncrease = 3
	mainAttribute = 'agility'
	damageModifier = 25
	skills = ['critical strike', 'exit wound', 'silent kill']