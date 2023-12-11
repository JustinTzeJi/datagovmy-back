from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Field(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)  # translatable
    description = models.TextField()  # translatable

    def __str__(self) -> str:
        return f"Field object ({self.name})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "title", "description"], name="unique_field"
            )
        ]


class RelatedDataset(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255)  # translatable
    description = models.TextField()  # translatable


class SiteCategory(models.Model):
    site = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"SiteCategory ({self.site} - {self.category} / {self.subcategory})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["site", "category", "subcategory"], name="unique_sitecategory"
            )
        ]


class DataCatalogueMeta(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    exclude_openapi = models.BooleanField()
    manual_trigger = models.CharField(max_length=255)
    site_category = models.ManyToManyField(SiteCategory)
    title = models.CharField(max_length=255)  # translatable
    description = models.TextField()  # translatable

    # FIXME: move to metadata?
    link_parquet = models.URLField()
    link_csv = models.URLField()
    link_preview = models.URLField()

    # filters
    frequency = models.CharField(max_length=50)
    geography = ArrayField(models.CharField(max_length=10, blank=True))
    demography = ArrayField(models.CharField(max_length=10, blank=True))
    dataset_begin = models.PositiveIntegerField()
    dataset_end = models.PositiveIntegerField()
    data_source = ArrayField(models.CharField(max_length=10, blank=True))

    # metadata & others
    fields = models.ManyToManyField(Field)
    data_as_of = models.CharField(max_length=50)
    last_updated = models.CharField(max_length=50, null=True)
    next_update = models.CharField(max_length=50, null=True)
    methodology = models.TextField()  # translatable
    caveat = models.TextField()  # translatable
    publication = models.TextField()  # translatable

    # FIXME: dataviz refactor to be foreign key?
    dataviz = ArrayField(models.JSONField())
    translations = models.JSONField()
    related_datasets = models.ManyToManyField(RelatedDataset)


class DataCatalogue(models.Model):
    """
    Each row in a dataframe that belongs to a data catalogue corresponds to a single row in this table.
    """

    catalogue_meta = models.ForeignKey(DataCatalogueMeta, on_delete=models.CASCADE)
    data = models.JSONField()

    class Meta:
        indexes = [models.Index(fields=["id"], name="data_catalogue_idx")]
