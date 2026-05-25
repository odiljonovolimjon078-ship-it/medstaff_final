from django.db import models

REGION_CHOICES = [
    ('toshkent', 'Toshkent'),
    ('andijon', 'Andijon'),
    ('fargona', 'Farg\'ona'),
    ('namangan', 'Namangan'),
    ('samarqand', 'Samarqand'),
    ('buxoro', 'Buxoro'),
    ('qashqadaryo', 'Qashqadaryo'),
    ('surxondaryo', 'Surxondaryo'),
    ('xorazm', 'Xorazm'),
    ('navoiy', 'Navoiy'),
    ('jizzax', 'Jizzax'),
    ('sirdaryo', 'Sirdaryo'),
    ('qoraqalpogiston', 'Qoraqalpog\'iston'),
]

HOSPITAL_TYPE_CHOICES = [
    ('davlat', 'Davlat kasalxonasi'),
    ('xususiy', 'Xususiy klinika'),
    ('poliklinika', 'Poliklinika'),
    ('shifoxona', 'Shifoxona'),
    ('tez yordam', 'Tez yordam markazi'),
]

POSITION_CHOICES = [
    ('shifokor', 'Shifokor'),
    ('hamshira', 'Hamshira'),
    ('jarroh', 'Jarroh'),
    ('laborant', 'Laborant'),
    ('radiolog', 'Radiolog'),
    ('stomatolог', 'Stomatolog'),
    ('pediatr', 'Pediatr'),
    ('kardiolog', 'Kardiolog'),
    ('nevropatolog', 'Nevropatolog'),
    ('anesteziolog', 'Anesteziolog'),
    ('farmatsevt', 'Farmatsevt'),
    ('psixiatr', 'Psixiatr'),
    ('boshqa', 'Boshqa'),
]

SHIFT_CHOICES = [
    ('kunduzgi', 'Kunduzgi'),
    ('tungi', 'Tungi'),
    ('aralash', 'Aralash'),
]


class Hospital(models.Model):
    name = models.CharField(max_length=200, verbose_name='Kasalxona nomi')
    hospital_type = models.CharField(max_length=50, choices=HOSPITAL_TYPE_CHOICES, verbose_name='Turi')
    region = models.CharField(max_length=50, choices=REGION_CHOICES, verbose_name='Viloyat')
    address = models.CharField(max_length=300, verbose_name='Manzil')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    email = models.EmailField(blank=True, verbose_name='Email')
    website = models.URLField(blank=True, verbose_name='Veb-sayt')
    bed_count = models.PositiveIntegerField(default=0, verbose_name='O\'rin soni')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kasalxona'
        verbose_name_plural = 'Kasalxonalar'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def staff_count(self):
        return self.staff.filter(is_active=True).count()


class Staff(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Ism')
    last_name = models.CharField(max_length=100, verbose_name='Familiya')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Otasining ismi')
    age = models.PositiveIntegerField(verbose_name='Yosh')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name='Lavozim')
    specialization = models.CharField(max_length=200, blank=True, verbose_name='Mutaxassislik')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE,
                                  related_name='staff', verbose_name='Kasalxona')
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Tajriba (yil)')
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES,
                              default='kunduzgi', verbose_name='Ish vaqti')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    email = models.EmailField(blank=True, verbose_name='Email')
    photo = models.ImageField(upload_to='staff/', blank=True, null=True, verbose_name='Rasm')
    salary = models.DecimalField(max_digits=12, decimal_places=0,
                                  null=True, blank=True, verbose_name='Maosh (so\'m)')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    hired_date = models.DateField(null=True, blank=True, verbose_name='Ishga kirgan sana')
    notes = models.TextField(blank=True, verbose_name='Izoh')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} — {self.get_position_display()}"

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)
