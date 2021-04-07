# In python classes don't introduce scope that means variable defined inside class can't be directly used.
# LEGB - Local, enclosed, global, built -in
# Local -- Inside the current function
# Enclosing -- Inside enclosing functions
# GLobal -- At top level of module
# Built-in -- In the special built-in modules

######################################################################################################################################################

# from shipping import *
class ShippingContainer:

    # Defining class Attributes
    next_serial = 1337;
    HEIGHT_FT = 10;
    WIDTH_FT = 12;
    # Defining Static Methods
    @staticmethod
    def _generate_serial():
        result = ShippingContainer.next_serial;
        ShippingContainer.next_serial += 1;
        return result;

    # Defining class Methods
    @classmethod
    def create_empty(cls, owner_code, length_ft, **kwargs):
        return cls(owner_code, length_ft, contents = [], **kwargs);

    @classmethod
    def create_with_items(cls, owner_code, length_ft, items, **kwargs):
        return cls(owner_code, length_ft, contents = list(items), **kwargs);

    ### How to choose b/w static and class methods, if you don't need class attribute go for static
    ### So even if in future you want to move method out of class could easily do so

    def __init__(self, owner_code, length_ft, contents, **kwargs):
        self.owner_code = owner_code;
        self.contents = contents;
        # Accessing class attribute can do with either self or class Name but preferable class Name
        # Accessing it via self will instance hiding wouldn't change class Attribute
        ## but if you want to use polymorphism use it on instance rather than class
        self.serial = self._generate_serial();
        self.length_ft = length_ft;

    ## It's not wise do this, so use template design pattern
    @property
    def volume_ft3(self):
        return self._calc_volume()

    def _calc_volume(self):
        return ShippingContainer.HEIGHT_FT * ShippingContainer.WIDTH_FT* self.length_ft;




### Inheritance 
## *args -- non key arguments    **kwargs -- key value arguments
class RefrigratorShippingContainer(ShippingContainer):
    
    MAX_CELSIUS = 4.0;
    FRIDGE_VOLUME_FT3 = 100;

    @staticmethod
    def _generate_serial():
        result = 1234;
        return result;

    def __init__(self, owner_code, length_ft, contents, *, celsius, **kwargs):
        super().__init__(owner_code, length_ft, contents, **kwargs);
        self.celsius = celsius;

    @property
    def celsius(self):
        return self._celsius;

    @property
    def fahrenheit(self):
        return RefrigratorShippingContainer._c_to_f(self.celsius);


    @celsius.setter
    def celsius(self, value):
        self._set_celsius(value);

    ## This method is introduced to avoid fset validation from derived class
    def _set_celsius(self, value):
        if value > RefrigratorShippingContainer.MAX_CELSIUS:
            raise ValueError('Temp too high');
        self._celsius = value;

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = RefrigratorShippingContainer._f_to_c(value);

    @staticmethod
    def _c_to_f(celsius):
        return (celsius)*9/5 +32;

    @staticmethod
    def _f_to_c(fahrenheit):
        return (fahrenheit -32) * 9/5;

    # overriding property having no setter
    ## It's not wise do this, so use template design pattern
    # @property
    # def volume_ft3(self):
    #     return (super().volume_ft3 - RefrigratorShippingContainer.FRIDGE_VOLUME_FT3);


    def _calc_volume(self):
        return super()._calc_volume() - RefrigratorShippingContainer.FRIDGE_VOLUME_FT3;



class HeatedRefrigratorShippingContainer(RefrigratorShippingContainer):

    MIN_CELSIUS = -20;

    ## Overriding property having setter in parent class in derived class
    # @RefrigratorShippingContainer.celsius.setter
    # def celsius(self, value):
    #     if(not (HeatedRefrigratorShippingContainer.MIN_CELSIUS <= value)):
    #         raise ValueError('Temperature too cold!');
    #     # Use fset method for ensuring validation for parent class to avoid repeated code.
    #     ## Avoid using fset because inheritance is from higher level you may not be able to do that
    #     ## Follow template design pattern to avoid this
    #     RefrigratorShippingContainer.celsius.fset(self, value);

    def _set_celsius(self, value):
        if (not (HeatedRefrigratorShippingContainer.MIN_CELSIUS <= value)):
            raise ValueError('Temperature too cold!');
        super()._set_celsius(value);




