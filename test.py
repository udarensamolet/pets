class Names:
    def __int__(self):
        self.first_name = 'first_name'
        self.last_name = None

    def get_user_name(self):
        if self.first_name and self.last_name:
            return self.first_name, self.last_name
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name


full = Names()
print(full.get_user_name())
