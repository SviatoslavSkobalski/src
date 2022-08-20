import effects

class GoBerserk:
	def __init__(self):
		self.effect = effects.DamageImmunity()
		self.manaCost = 5
		
class MightyPunch:
	def __init__(self):
		self.manaCost = 5
		self.multiplier = 3

class BlowTheHeadOff:
	def __init__(self):
		self.manaCost = 10
		self.damage = 250
		self.chance = 25

class NatureHeal:
	def __init__(self):
		self.effect = effects.Heal()
		self.manaCost = 10

class Fireball:
	def __init__(self):
		self.effect = effects.Burn()
		self.manaCost = 15
		self.damage = 200

class HellFromTheSky:
	def __init__(self):
		self.manaCost = 100
		self.damage = 250
		self.chance = 25

class CriticalStrike:
	def __init__(self):
		self.multiplier = 3.5

class ExitWound:
	def __init__(self):
		self.effect = effects.Bleeding()
		self.damage = 150

class SilentKill:
	def __init__(self):
		self.manaCost = 100
		self.damage = 250
		self.chance = 25