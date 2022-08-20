from fractions import Fraction
from common import attributeModifiers

class Player:
	def __init__(self, name, attributes, archetype):
		self.name = name
		self.attributes = attributes
		self.archetype = archetype
		self.level = 1
		self.experience = 0

	#use to get an amount of full hero hp
	def calculateHealthPoints(self):
		return self.attributes['strenght'] * attributeModifiers['strenghtAttributeModifier']

	#use to get an amount of full hero mana	
	def calculateManaPoints(self):
		return self.attributes['intelligence'] * attributeModifiers['intelligenceAttributeModifier']

	#use to set an armor vale
	def calculateArmor(self):
		foo = Fraction(1, 10)
		self.armor = self.attributes['agility'] * foo
		return self.armor

	#use to set an magicResistance vale
	def calculateMagicResistance(self):
		foo = Fraction(1, 10)
		return self.attributes['intelligence'] * foo

	#use to set damage
	def calculateDamage(self):
		self.damage = self.attributes[self.archetype.mainAttribute] * self.archetype.damageModifier
		return self.damage

	#use to calculate base heal
	def calculateBaseHeal(self):
		foo = Fraction(1, 10)
		return self.attributes['strenght'] * foo