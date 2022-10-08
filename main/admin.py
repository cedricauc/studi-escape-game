from django.contrib import admin

from main.models import User, Level, Image, Room, Scenario, Cart, Booking, Game, Discount, ScenarioRoomClue, \
    TicketCategory, TicketQuestion, TicketAnswer


class UserAdmin(admin.ModelAdmin):
    exclude = []
    fieldsets = (
        (None, {"fields": ('username', 'email', 'password', 'is_superuser', 'is_staff', 'is_active', 'role',)}),
        ("Détails", {"fields": ('first_name', 'last_name', 'last_login',)}),
    )
    list_display = ("username", "role")
    list_filter = ("username", "role")
    list_editable = ()
    ordering = ("-username",)
    search_fields = ("username", "role")


class ScenarioAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ('title', 'description', 'duration', 'level', 'rooms',)}),
        ("Détails", {"fields": ('min_participant', 'max_participant', 'price_participant', 'images',)}),
    )
    list_display = ("title", "duration", "price_participant", "level")
    list_filter = ("title", "duration", "level")
    list_editable = ("level", "duration", "price_participant")
    ordering = ("-title",)
    search_fields = ("title", "duration", "price_participant")


class CartAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ("scenario", "created_date", "start_date", "participant")
    list_filter = ("scenario", "created_date")
    list_editable = ("scenario",)
    ordering = ("-created_date",)
    search_fields = ("scenario", "start_date",)
    list_display_links = None


class BookingAdmin(admin.ModelAdmin):
    exclude = []
    fieldsets = (
        (None, {"fields": ('scenario', 'booking_number', 'participant', 'start_date', 'total_amount',)}),
        ("Détails", {"fields": ('user', 'is_canceled',)}),
    )
    list_display = ("scenario", "start_date", "participant",)
    list_filter = ("scenario", "start_date",)
    list_editable = ("scenario", "start_date",)
    ordering = ("-start_date",)
    search_fields = ("scenario", "start_date",)
    list_display_links = None


class GameAdmin(admin.ModelAdmin):
    exclude = []  
    fieldsets = (
        (None, {"fields": ('booking', 'start_time', 'end_time',)}),
    )
    list_display = ("booking", "start_time", "end_time")
    list_filter = ("booking", "start_time",)
    list_editable = ("booking",)
    ordering = ("-start_time",)
    search_fields = ("booking", "start_time",)
    list_display_links = None


class DiscountAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ("discount", "step")
    list_filter = ("discount",)
    list_editable = ("discount",)
    ordering = ("-discount",)
    search_fields = ("discount",)
    list_display_links = None


class ScenarioRoomClueAdmin(admin.ModelAdmin):
    exclude = []  
    fieldsets = (
        (None, {"fields": ('scenario', 'room', 'clue',)}),
    )
    list_display = ("scenario", "room")
    list_filter = ("scenario", "room")
    list_editable = ("scenario", "room")
    ordering = ("-scenario",)
    search_fields = ("scenario", "room")
    list_display_links = None


class TicketQuestionAdmin(admin.ModelAdmin):
    exclude = []  
    fieldsets = (
        (None, {"fields": ('author', 'question', 'category',)}),
    )
    list_display = ("category", "created_date", "author")
    list_filter = ("category", "created_date")
    list_editable = ("category",)
    ordering = ("-created_date",)
    search_fields = ("category", "created_date")
    list_display_links = None


class TicketAnswerAdmin(admin.ModelAdmin):
    exclude = []  
    fieldsets = (
        (None, {"fields": ('answer', 'question',)}),
    )
    list_display = ("question", "created_date",)
    list_filter = ("question", "created_date")
    list_editable = ("question",)
    ordering = ("-created_date",)
    search_fields = ("question", "created_date")
    list_display_links = None


admin.site.register(User, UserAdmin)

admin.site.register(Scenario, ScenarioAdmin)

admin.site.register(Level)

admin.site.register(Booking, BookingAdmin)

admin.site.register(Image)

admin.site.register(Room)

admin.site.register(Cart, CartAdmin)

admin.site.register(Game, GameAdmin)

admin.site.register(Discount, DiscountAdmin)

admin.site.register(ScenarioRoomClue, ScenarioRoomClueAdmin)

admin.site.register(TicketCategory)

admin.site.register(TicketQuestion, TicketQuestionAdmin)

admin.site.register(TicketAnswer, TicketAnswerAdmin)
