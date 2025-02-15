from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from members.models import Department
from members.models import ActivityParticipant


class ActivityParticipantInline(admin.TabularInline):
    model = ActivityParticipant
    extra = 0
    fields = ("person",)
    readonly_fields = fields
    raw_id_fields = ("person",)

    def get_queryset(self, request):
        return ActivityParticipant.objects.all()


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "union_link",
        "department_link",
        "activitytype",
        "start_end",
        "open_invite",
        "price_in_dkk",
        "seats_total",
        "seats_used",
        "seats_free",
        "age",
    )

    date_hierarchy = "start_date"
    search_fields = (
        "name",
        "department__union__name",
        "department__name",
        "description",
    )
    readonly_fields = ("seats_left", "participants")
    list_per_page = 20
    raw_id_fields = (
        "union",
        "department",
    )
    list_filter = (
        "department__union__name",
        "department__name",
        "open_invite",
        "activitytype",
    )
    save_as = True
    inlines = [ActivityParticipantInline]

    def startend(self, obj):
        return str(obj.start_date) + " - " + str(obj.end_date)

    startend.short_description = "Periode"

    def age(self, obj):
        return str(obj.min_age) + " - " + str(obj.max_age)

    age.short_description = "Alder"

    def start_end(self, obj):
        return str(obj.start_date) + " - " + str(obj.end_date)

    start_end.short_description = "Periode"

    def age(self, obj):
        return str(obj.min_age) + " - " + str(obj.max_age)

    age.short_description = "Alder"

    def union_link(self, item):
        url = reverse("admin:members_union_change", args=[item.department.union_id])
        link = '<a href="%s">%s</a>' % (url, item.department.union.name)
        return mark_safe(link)

    union_link.short_description = "Forening"
    union_link.admin_order_field = "department__union__name"

    def department_link(self, item):
        url = reverse("admin:members_department_change", args=[item.department_id])
        link = '<a href="%s">%s</a>' % (url, item.department.name)
        return mark_safe(link)

    department_link.short_description = "Afdeling"
    department_link.admin_order_field = "department__name"

    def seats_total(self, obj):
        return str(obj.max_participants)

    seats_total.short_description = "Total"

    def seats_used(self, obj):
        return str(obj.activityparticipant_set.count())

    seats_used.short_description = "Besat"

    def seats_free(self, obj):
        return str(obj.max_participants - obj.activityparticipant_set.count())

    seats_free.short_description = "Ubesat"

    # Only view activities on own department
    def get_queryset(self, request):
        qs = super(ActivityAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        departments = Department.objects.filter(adminuserinformation__user=request.user)
        return qs.filter(department__in=departments)

    # Only show own departments when creating new activity
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department" and not request.user.is_superuser:
            kwargs["queryset"] = Department.objects.filter(
                adminuserinformation__user=request.user
            )
        return super(ActivityAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    fieldsets = [
        (
            "Afdeling",
            {
                "description": "<p>Du kan ændre afdeling for aktiviteten ved at skrive afdelings-id, eller tryk på søg-ikonet og i det nye vindue skal du finde afdelingen, for derefter at trykke på ID i første kolonne.</p>",
                "fields": ("department",),
            },
        ),
        (
            "Forening",
            {
                "description": "<p><b>Bemærk:</b> Denne værdi bruges kun til foreningsmedlemsskab/støttemedlemsskab.</p>",
                "fields": ("union",),
            },
        ),
        (
            "Aktivitet",
            {
                "description": "<p>Aktivitetsnavnet skal afspejle aktivitet samt tidspunkt. F.eks. <em>Forårssæson 2018</em>.</p><p>Tidspunkt er f.eks. <em>Onsdage 17:00-19:00</em></p>",
                "fields": (
                    (
                        "name",
                        "activitytype",
                    ),
                    "open_hours",
                    "description",
                    (
                        "start_date",
                        "end_date",
                    ),
                    "member_justified",
                ),
            },
        ),
        (
            "Lokation og ansvarlig",
            {
                "description": "<p>Adresse samt ansvarlig kan adskille sig fra afdelingens informationer (f.eks. et gamejam der foregår et andet sted).</p>",
                "fields": (
                    (
                        "responsible_name",
                        "responsible_contact",
                    ),
                    (
                        "streetname",
                        "housenumber",
                        "floor",
                        "door",
                    ),
                    (
                        "zipcode",
                        "city",
                        "placename",
                    ),
                ),
            },
        ),
        (
            "Tilmeldingsdetaljer",
            {
                "description": '<p>Tilmeldingsinstruktioner er tekst der kommer til at stå på betalingsformularen på tilmeldingssiden. Den skal bruges til at stille spørgsmål, som den, der tilmelder sig, kan besvare ved tilmelding.</p><p>Fri tilmelding betyder, at alle, når som helst kan tilmelde sig denne aktivitet - efter "først til mølle"-princippet. Dette er kun til aktiviteter og klubaften-forløb/sæsoner i områder, hvor der ikke er nogen venteliste. </p><p>Alle aktiviteter med fri tilmelding kommer til at stå med en stor "tilmeld" knap på medlemssiden. <b>Vi bruger typisk ikke fri tilmelding - spørg i Slack hvis du er i tvivl!</b></p>',
                "fields": (
                    "instructions",
                    (
                        "signup_closing",
                        "open_invite",
                    ),
                    "price_in_dkk",
                    (
                        "max_participants",
                        "participants",
                        "seats_left",
                    ),
                    (
                        "min_age",
                        "max_age",
                    ),
                ),
            },
        ),
    ]
