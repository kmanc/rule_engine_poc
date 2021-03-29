def value_is(instance_value, indicator_dict):
	return indicator_dict.get(instance_value)


def value_in(instance_value, indicator_dict):
	for indicator_value, label in indicator_dict.items():
		if indicator_value in instance_value:
			return label


class LowA:
	is_dictionary = dict()

	def __init__(self, value: str):
		self.value = value

	def value_is(self):
		return value_is(self.value, LowA.is_dictionary)


class LowB:
	is_dictionary = dict()
	in_dictionary = dict()

	def __init__(self, value: str):
		self.value = value

	def value_is(self):
		return value_is(self.value, LowB.is_dictionary)

	def value_in(self):
		return value_in(self.value, LowB.in_dictionary)


class HighA:
	def __init__(self, a, b, c):
		self.a = LowA(a)
		self.b = LowB(b)
		self.c = c


a = HighA("101010101", "cmd.exe", "2021-04-01")
b = HighA("010101010", "putty.exe", "2021-03-31")
instances = [a, b]
low_a_is_indicators = {"101010101": "Indicator1", "cmd.exe": "Indicator2"}
path_in_indicators = {".zip": "Indicator3", ".exe": "Indicator4"}
setattr(LowA, "is_dictionary", low_a_is_indicators)
setattr(LowB, "in_dictionary", path_in_indicators)


def is_custom(custom_or_not):
	return custom_or_not.__class__.__module__ != 'builtins'


def recursive_unclass(class_instance):
	as_dict = dict()
	for key, value in vars(class_instance).items():
		if is_custom(value):
			as_dict[key] = recursive_unclass(value)
		elif key == "value":
			return value
		else:
			as_dict[key] = value
	return as_dict


for instance in instances:
	attributes = vars(instance).values()
	for attribute in attributes:
		if not is_custom(attribute):
			continue
		functions = (func for func in dir(attribute) if callable(getattr(attribute, func)) and not func.startswith("__"))
		for function in functions:
			result = getattr(attribute, function)()
			if result is not None:
				instance_dict = recursive_unclass(instance)
				print(f"{result} found in {instance_dict}")
