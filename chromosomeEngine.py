import numpy as np


class chromosomeEngine:
	def __init__(self, fieldsDescription):
		self.fieldsDescription = fieldsDescription

	def getRandChromosome(self):
		chromosome = {}
		for field in self.fieldsDescription:
			chromosome[field] = np.random.randint(self.fieldsDescription[field]["lowerBound"],self.fieldsDescription[field]["upperBound"])/self.fieldsDescription[field]["resolution"]

		# newChr["margin"]["sell"] = np.random.randint(0,2000)/100.0
		return chromosome

	def mixChromosomes(self, chr1, chr2):
		chromosome = {}
		for field in chr1:
			# 1/3 probability to get allele 1, 1/3 to get allele 2, 1/3 probability to get the average of both
			randomInt = np.random.randint(0,100)
			if randomInt < 33:
				chromosome[field] = chr1[field]
			elif randomInt < 64:
				chromosome[field] = chr2[field]
			else:
				chromosome[field] = (chr1[field] + chr2[field]) / 2.0
		return chromosome



