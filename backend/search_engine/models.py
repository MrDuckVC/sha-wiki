from django.db import models


class Prefectures(models.Model):
    # prefectureName from xml, name of the prefecture.
    name = models.CharField(max_length=128, db_comment="Name of the prefecture.")
    # prefectureCode from xml, unique number of the prefecture.
    code = models.CharField(unique=True, max_length=2, db_comment="Unique number of the prefecture.")
    # enPrefectureName from xml, name of the prefecture in English.
    en_name = models.CharField(max_length=128, db_comment="Name of the prefecture in English.")

    created_at = models.DateTimeField(blank=True, auto_now_add=True, db_comment="Created at.")
    updated_at = models.DateTimeField(blank=True, auto_now=True, db_comment="Updated at.")

    class Meta:
        db_table = "prefectures"


class Cities(models.Model):
    # cityName from xml, name of the city.
    name = models.CharField(max_length=128, db_comment="Name of the city.")
    # cityCode from xml, unique number of the city.
    code = models.SmallIntegerField(db_comment="Unique number of the city.")
    # enCityName from xml, name of the city in English.
    en_name = models.CharField(max_length=128, blank=True, null=True, db_comment="Name of the city in English.")

    created_at = models.DateTimeField(blank=True, auto_now_add=True, db_comment="Created at.")
    updated_at = models.DateTimeField(blank=True, auto_now=True, db_comment="Updated at.")

    class Meta:
        db_table = "cities"


class Corporations(models.Model):
    # corporateNumber from xml, unique number for each company in Japan to identify it.
    number = models.CharField(unique=True, max_length=13, db_comment="Unique number for each company in Japan to identify it.")
    # process from xml, consist of 2 numbers (02, 81, 32, ...), not sure what it is.
    process = models.CharField(max_length=2, db_comment="Consist of 2 numbers (02, 81, 32, ...), not sure what it is.")
    # correct from xml, not sure what it is.
    correct = models.BooleanField(db_comment="Not sure what it is.")
    # updateDate from xml, date of update of the record in import file.
    update_date = models.DateField(db_comment="Date of update of the record in import file.")
    # changeDate from xml, date of change of the record in import file.
    change_date = models.DateField(db_comment="Date of change of the record in import file.")
    # name from xml, name of the company.
    name = models.CharField(max_length=256, db_comment="Name of the company.")
    # nameImageId from xml, image of the company name (https://www.houjin-bangou.nta.go.jp/image?imageid=<nameImageId>).
    name_image_id = models.CharField(max_length=8, blank=True, null=True, db_comment="Image of the company name (https://www.houjin-bangou.nta.go.jp/image?imageid=<nameImageId>).")
    # kind from xml, not sure what it is.
    kind = models.SmallIntegerField(db_comment="Not sure what it is.")
    # streetNumber from xml, name of the street.
    street_number = models.CharField(max_length=128, blank=True, null=True, db_comment="Name of the street.")
    # addressImageId from xml, image of the company address (https://www.houjin-bangou.nta.go.jp/image?imageid=<addressImageId>).
    address_image_id = models.CharField(max_length=8, blank=True, null=True, db_comment="Image of the company address (https://www.houjin-bangou.nta.go.jp/image?imageid=<addressImageId>).")
    # postCode from xml, postal code of the company.
    post_code = models.CharField(max_length=7, blank=True, null=True, db_comment="Postal code of the company.")
    # addressOutside from xml, address of the company outside of Japan.
    address_outside = models.CharField(max_length=512, blank=True, null=True, db_comment="Address of the company outside of Japan.")
    # addressOutsideImageId from xml, image of the company address outside of Japan (https://www.houjin-bangou.nta.go.jp/image?imageid=<addressOutsideImageId>).
    address_outside_image_id = models.CharField(max_length=8, blank=True, null=True, db_comment="Image of the company address outside of Japan (https://www.houjin-bangou.nta.go.jp/image?imageid=<addressOutsideImageId>).")
    # closeDate from xml, date of the company closing.
    close_date = models.DateField(blank=True, null=True, db_comment="Date of the company closing.")
    # closeCause from xml, cause code of the company closing.
    close_cause = models.CharField(max_length=2, blank=True, null=True, db_comment="Cause code of the company closing.")
    # successorCorporateNumber from xml, old corporate number of the company.
    successor_number = models.CharField(max_length=13, blank=True, null=True, db_comment="Old corporate number of the company.")
    # changeCause from xml, cause code of the company change.
    change_cause = models.TextField(blank=True, null=True, db_comment="Cause code of the company change.")
    # assignmentDate from xml, date of the company assignment (date of creation of corporate number).
    assignment_date = models.DateField(db_comment="Date of the company assignment (date of creation of corporate number).")
    # latest from xml, not sure what it is.
    latest = models.BooleanField(db_comment="Not sure what it is.")
    # enName from xml, name of the company in English.
    en_name = models.CharField(max_length=256, blank=True, null=True, db_comment="Name of the company in English.")
    # enAddressOutside from xml, address of the company outside of Japan in English.
    en_address_outside = models.CharField(max_length=128, blank=True, null=True, db_comment="Address of the company outside of Japan in English.")
    # furigana from xml, syllabic writing of the company name.
    furigana = models.CharField(max_length=256, blank=True, null=True, db_comment="Syllabic writing of the company name.")
    # hihyoji from xml, hidden or not.
    hihyoji = models.BooleanField(db_comment="Hidden or not.")

    # Prefecture (region of Japan) and city of the company.
    prefecture = models.ForeignKey("Prefectures", models.DO_NOTHING, blank=True, null=True, db_comment="Prefecture (region of Japan) of the company.")
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True, db_comment="City of the company.")

    created_at = models.DateTimeField(blank=True, auto_now_add=True, db_comment="Created at.")
    updated_at = models.DateTimeField(blank=True, auto_now=True, db_comment="Updated at.")

    class Meta:
        db_table = "corporations"

        # Add indexing to improve performance.
        indexes = [
            models.Index(fields=[
                "number",
                "name",
            ])
        ]

    def __str__(self):
        return self.name

    @property
    def address(self):
        not_available = "N/A"
        return "{prefecture}; {city}; {street_number}; 〒 {post_code}".format(
            prefecture=self.prefecture.name if self.prefecture else not_available,
            city=self.city.name if self.city else not_available,
            street_number=self.street_number if self.street_number else not_available,
            post_code=self.post_code if self.post_code else not_available,
        )
