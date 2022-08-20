from pickle import FALSE
import random
import time
import archetypes
from character import Player
from common import fakeNames, archetypeNames
import skills 
import effects

class ArenaManager:
	def __init__(self):
		bot = BotManager.createBot()
		self.enemy = bot

	def start(self):
		playerManager = PlayerManager()
		player = playerManager.getPlayerCharacter()

		time.sleep(1)

		fightManager = FightManager(player, self.enemy)

		print('The fight between ', self.enemy.name, ' and ', player.name, ' begins now!')

		fightManager.fight()

class BotManager:
	def createBot():
		pointsAmount = 12
		strenght = random.randrange(1, pointsAmount)
		pointsAmount = pointsAmount - strenght
		agility = random.randrange(1, pointsAmount)
		pointsAmount = pointsAmount - agility

		attributes = {
			'strenght' : strenght,
			'agility' : agility,
			'intelligence' : pointsAmount
		}

		nameId = random.randrange(0, 3)
		name = fakeNames[nameId]

		archetypeId = random.randrange(0, 2)
		if archetypeId == 0:
			archetype = archetypes.Warrior()
		if archetypeId == 1:
			archetype = archetypes.Shaman()
		if archetypeId == 2:
			archetype = archetypes.Trickster()

		bot = Player(name, attributes, archetype)
		return bot

class FightManager:
	def __init__(self, player, enemy):
		player.hp = player.calculateHealthPoints()
		player.mp = player.calculateManaPoints()
		player.dmg = player.calculateDamage()
		player.baseHeal = player.calculateBaseHeal()
		player.armor = player.calculateArmor()
		player.magicResistance = player.calculateMagicResistance()
		player.damageImmunity = False
		player.effects = []

		enemy.hp = enemy.calculateHealthPoints()
		enemy.mp = enemy.calculateManaPoints()
		enemy.dmg = enemy.calculateDamage()
		enemy.baseHeal = enemy.calculateBaseHeal()
		enemy.armor = enemy.calculateArmor()
		enemy.magicResistance = enemy.calculateMagicResistance()
		enemy.damageImmunity = False
		enemy.effects = []

		self.player = player
		self.enemy = enemy

		self.playerEffectsManager = EffectsManager(player)
		self.enemyEffectsManager = EffectsManager(enemy)
		self.playerSkillsManager = SkillsManager(player, enemy)
		self.enemySkillsManager = SkillsManager(enemy, player)
		self.playerMagicMachine = MagicMachine(player, enemy)
		self.enemyMagicMachine = MagicMachine(enemy, player)

	def fight(self):
		while self.player.hp > 0 and self.enemy.hp > 0:

			self.playerEffectsManager.applyEffects()
			self.playerMagicMachine.doMagic()

			pdmg = 0 if self.enemy.damageImmunity else self.player.dmg * self.enemy.armor
			
			self.enemy.hp -= pdmg
			
			time.sleep(1)
			print(self.enemy.name, ' suffered: ', pdmg, ' damage | ', self.enemy.hp, ' has left') if self.enemy.hp > 0 else print(self.enemy.name, ' sufferd mortal wound')
			time.sleep(1)
			
			self.enemy.hp += self.enemy.baseHeal
			
			time.sleep(1)
			print(self.enemy.name, ' healed ', self.enemy.baseHeal,' | ', self.player.hp, ' has left')
			time.sleep(1)
			
			self.enemyEffectsManager.applyEffects()		
			self.enemyMagicMachine.doMagic()

			edmg = 0 if self.player.damageImmunity else self.enemy.dmg * self.enemy.armor
			self.player.hp -= edmg
			time.sleep(1)
			print (self.player.name, ' suffered: ', edmg, ' damage | ', self.player.hp, ' has left') if self.player.hp > 0 else print(self.player.name, ' suffered mortal wound')
			time.sleep(1)
			
			self.player.hp += self.enemy.baseHeal
			
			time.sleep(1)
			print(self.player.name, ' healed ', self.player.baseHeal, ' |', self.player.hp, ' has left')
			time.sleep(1)
		else:
			print('You had win the fight') if self.player.hp > self.enemy.hp else print('You suffered loss from ', self.enemy.name)

class EffectsManager:
	def __init__(self, character):
		self.character = character

	def checkForEffects(self):
		return len(self.character.effects) != 0

	def applyEffects(self):
		if self.checkForEffects() == True:
			for x in self.character.effects:
				if x.duration == 0:
					self.character.effects.remove(x)
				elif x.duration == 0 and type(x) == effects.DamageImmunity:	
					self.character.damageImmunity = False

				if x.duration > 0 and type(x) == effects.Bleeding:
					x.duration -= 1
					self.character.hp = self.character.hp - x.damage
					print(self.character.name,  ' suffered ', x.damage, 'damage from bleeding')
					time.sleep(1)
				elif x.duration > 0 and type(x) == effects.Burn:
					x.duration -= 1
					self.character.hp = self.character.hp - x.damage
					print(self.character.name,  ' suffered ', x.damage, 'damage from burn')
					time.sleep(1)
				elif x.duration > 0 and type(x) == effects.DamageImmunity:
					x.duration -= - 1
					self.character.damageImmunity = True
					print(self.character.name, ' is damage immune for next ', x.duration, ' rounds')
					time.sleep(1)
				elif x.duration > 0 and type(x) == effects.Heal:
					x.duration -= 1
					self.character.hp = self.character.hp + x.heal
					print(self.character.name,  ' healed by ', x.heal)
					time.sleep(1)

class SkillsManager:
	def __init__(self, player, enemy):
		self.player = player
		self.enemy = enemy
	
	def useGoBerserk(self):
		time.sleep(1)
		print(self.player.name, ' is going Berserk')
		goBerserk = skills.GoBerserk()
		if self.player.mp > goBerserk.manaCost:
			self.player.mp = self.player.mp - goBerserk.manaCost
			if goBerserk.effect not in self.player.effects:
				self.player.effects.append(goBerserk.effect)
			print('not enough mana')

	def useMightyPunch(self):
		print(self.player.name, ' is doing a Mighty Punch')
		time.sleep(1)
		mightyPunch = skills.MightyPunch()
		if self.player.mp > mightyPunch.manaCost:
			self.player.mp = self.player.mp - mightyPunch.manaCost
			multipliedDmg = self.player.dmg * mightyPunch.multiplier
			dmgDone = multipliedDmg * self.enemy.armor
			self.enemy.hp = self.enemy.hp - dmgDone
			print(self.enemy.name, ' suffered ', dmgDone, ' from Mighty Punch')
			time.sleep(1)
		else: 
			time.sleep(1)
			print('not enough mana')

	def useBlowTheHeadOff(self):
		time.sleep(1)
		print(self.player.name, ' is doing a Blow a Head Off!')
		time.sleep(1)
		blowTheHeadOff = skills.BlowTheHeadOff()
		if self.player.mp > blowTheHeadOff.manaCost:
			self.player.mp -= blowTheHeadOff.manaCost
			chance = random.randrange(1, 100)
			if chance < blowTheHeadOff.chance:
				self.enemy.hp = 0
				print('Instant kill!')
			dmgDone = blowTheHeadOff.damage * self.enemy.armor
			self.enemy.hp = self.enemy.hp - dmgDone
			time.sleep(1)
			print('Enemy suffered ', dmgDone, ' from BlowTheHeadOff')
			time.sleep(1)
		else:
			time.sleep(1)
			print('not enough mana')

	def useNatureHeal(self):
		print(self.player.name, ' healing himself')
		natureHeal = skills.NatureHeal()
		if self.player.mp > natureHeal.manaCost:
			self.player.mp -= natureHeal.manaCost
			self.player.effects.append(natureHeal.effect)
		else:
			print('not enough mana')

	def useFireball(self):
		time.sleep(1)
		print(self.player.name, ' is casting a fireball')
		time.sleep(1)
		fireBall = skills.Fireball()
		if self.player.mp > fireBall.manaCost:
			self.player.mp -= fireBall.manaCost
			self.enemy.effects.append(fireBall.effect)
			dmgDone = fireBall.damage * self.enemy.magicResistance
			self.enemy.hp = self.enemy.hp - dmgDone
			time.sleep(1)
			print('Enemy suffered ', dmgDone, ' from fireball')
			time.sleep(1)
		else:
			time.sleep(1)
			print('not enough mana')
			time.sleep(1)

	def useHellFromTheSky(self):
		time.sleep(1)
		print(self.player.name, ' is putting Hell upon us all')
		time.sleep(1)
		hellFromTheSky = skills.HellFromTheSky()
		if self.player.mp > hellFromTheSky.manaCost:
			self.player.mp -= hellFromTheSky.manaCost
			chance = random.randrange(1, 100)
			if chance < hellFromTheSky.chance:
				self.enemy.hp = 0
				time.sleep(1)
				print('Instant kill!')
				time.sleep(1)
			dmgDone = hellFromTheSky.damage * self.enemy.magicResistance
			self.enemy.hp = self.enemy.hp - dmgDone
			time.sleep(1)
			print('Enemy suffered ', dmgDone, ' from Hell from the Sky')
			time.sleep(1)
		else:
			time.sleep(1)
			print('not enough mana')

	def useCriticalStrike(self):
		time.sleep(1)
		print(self.player.name, ' does a critical strike')
		time.sleep(1)
		criticalStrike = skills.CriticalStrike()
		multipliedDmg = self.player.dmg * criticalStrike.multiplier
		dmgDone = multipliedDmg * self.enemy.armor
		self.enemy.hp = self.enemy.hp - dmgDone
		time.sleep(1)
		print(self.enemy.name, ' suffered ', dmgDone, ' from sritical strike')
		time.sleep(1)

	def useExitWound(self):
		time.sleep(1)
		print(self.player.name, ' make an exit wound')
		time.sleep(1)
		exitWound = skills.ExitWound()
		self.enemy.effects.append(exitWound.effect)
		dmgDone = exitWound.damage * self.enemy.armor
		self.enemy.hp = self.enemy.hp - dmgDone
		time.sleep(1)
		print(self.enemy.name, ' suffered ', dmgDone, ' from an exit wound')
		time.sleep(1)

	def useSilentKill(self):
		time.sleep(1)
		print(self.player.name, ' goes with silent kill')
		time.sleep(1)
		silentKill = skills.SilentKill()
		if self.player.mp > silentKill.manaCost:
			self.player.mp -= silentKill.manaCost
			chance = random.randrange(1, 100)
			if chance < silentKill.chance:
				self.enemy.hp = 0
				time.sleep(1)
				print('Instant kill!')
				time.sleep(1)
			dmgDone = silentKill.damage * self.enemy.armor
			self.enemy.hp = self.enemy.hp - dmgDone
			time.sleep(1)
			print(self.enemy.name, ' suffered ', dmgDone, ' from Silent Kill')
			time.sleep(1)
		else:
			time.sleep(1)
			print('not enough mana')
			time.sleep(1)

class PlayerManager:
	def getCharacterDetails(self):
		maxPointsAvailable = 12
		characterName = input("Enter your characters name: ")
		archetype = input('Select your characters archetype from Warrior, Shaman or Trickster: ')
		print('You are given a 12 points to fill in your characters attributes, choose wisely')
		strenght = input('Set your characters strenght: ')
		maxPointsAvailable = maxPointsAvailable - int(strenght)
		print(maxPointsAvailable, 'points left')
		agility = input('Set your characters agility: ')
		maxPointsAvailable = maxPointsAvailable - int(agility)
		print('Points left is assigned to intelligence')
		intelligence = maxPointsAvailable
		return [characterName, archetype, strenght, agility, intelligence]

	def getPlayerCharacter(self):
		results = self.getCharacterDetails()

		characterName = results[0]
		archetypeCode = results[1]
		strenght = results[2]
		agility = results[3]
		intelligence = results[4]

		intStr = int(strenght)
		intAgil = int(agility)
		intIntelligence = int(intelligence)

		print('Your character is a ', archetypeCode, ' Named', characterName, 'With ', strenght, ' strenght', agility, ' agility', intelligence, ' intelligence')

		if archetypeCode == archetypeNames[0]:
			archetype = archetypes.Warrior()
		elif archetypeCode == archetypeNames[1]:
			archetype = archetypes.Shaman()
		elif archetypeCode == archetypeNames[2]:
			archetype = archetypes.Trickster()
		
		attributes = {
			'strenght' : intStr,
			'agility' : intAgil,
			'intelligence' : intIntelligence
			}

		return Player(characterName, attributes, archetype)

class MagicMachine:
	def __init__(self, player, enemy):
		self.character = player
		self.skillsManager = SkillsManager(player, enemy)

	def doMagic(self):
		castChanceLuck = random.randrange(1, 50)
		castChanceUnLuck = random.randrange(1, 25)
		skill = random.randrange(0, 2)
		
		if type(self.character.archetype) == archetypes.Warrior:
			if castChanceLuck > castChanceUnLuck:
				if skill == 0:
					self.skillsManager.useGoBerserk()
				if skill == 1:
					self.skillsManager.useMightyPunch()
				if skill == 2:
					self.skillsManager.useBlowTheHeadOff()

		if type(self.character.archetype) == archetypes.Shaman:
			if castChanceLuck > castChanceUnLuck:
				if skill == 0:
					self.skillsManager.useNatureHeal()
				if skill == 1:
					self.skillsManager.useFireball()
				if skill == 2:
					self.skillsManager.useHellFromTheSky()

		if type(self.character.archetype) == archetypes.Trickster:
			if castChanceLuck > castChanceUnLuck:
				if skill == 0:
					self.skillsManager.useCriticalStrike()
				if skill == 1:
					self.skillsManager.useExitWound()
				if skill == 2:
					self.skillsManager.useSilentKill()
