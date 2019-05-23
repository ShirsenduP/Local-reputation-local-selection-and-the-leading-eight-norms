from math import inf

class Validator():
	def __init__(self):
		pass

	def checkListTypes(self, listOfThings, requiredType):
		"""Check if every thing in 'listOfThings' is of type 'requiredType'."""

		for thing in listOfThings:
			if type(thing) != requiredType:
				raise TypeError(str(listOfThings) + " contains objects that are not " + str(requiredType) + ".")
		
	def checkRangeOfValuesInList(self, listOfThings, bounds, edges=True):
		"""Raise an exception if the given 'listOfThings' contains values that are outside the range defined by the list 'bounds' where 'edges' is a boolean clarifying whether the bounds are inclusive or exclusive of the bound values themselves."""
		
		if edges:
			for thing in listOfThings:
				if thing < bounds[0] or thing > bounds[1]:
					raise ValueError(str(listOfThings) + " contains values that are out of the range " + str(bounds))
		else:
			for thing in listOfThings:
				if thing <= bounds[0] or thing >= bounds[1]:
					raise ValueError(str(listOfThings) + " contains values that are out of the range " + str(bounds))

	def checkPrisonerDilemnaParameters(self, pdBenefit, pdCost):
		"""Check if the parameters of the prisoner's dilemna are valid, that is the benefit is greater and not equal to the cost of cooperation and that they are positive values."""

		if pdBenefit <= pdCost:
			raise ValueError("The payoff of the Prisoner's Dilemna game must be greater than the cost of cooperation.")
		if pdBenefit<0 or pdCost<0:
			raise ValueError("The payoff and cost must be positive values.")

	def checkValidDistribution(self, distribution):
		"""Check that the distribution of population strategies is valid."""

		if sum(distribution) != 1:
			raise ValueError(f"Distribution {distribution} must sum to 1.")

	def checkMaxPeriods(self, maxPeriods):
		"""Check that the number of timesteps allowed is in a suitable range"""
		self.checkRangeOfValuesInList([maxPeriods], [0, inf], edges=False)

	def checkNumeric(self, values):
		for value in values:
			if not str(value).isnumeric():
				raise TypeError(f"The value {value} must be numeric.")