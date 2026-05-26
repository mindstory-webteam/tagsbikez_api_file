"""
apps/api/serializers.py
All DRF serializers for TagsBikez.
Sections: Home | Events | Gallery | Categories | Motorcycles | Careers
"""

from rest_framework import serializers
from apps.categories.models import ProductCategory
from apps.motorcycles.models import (
    MotorcycleProduct,
    ProductColor,
    ProductTopAbout,
    ProductFeatureSection,
)
from apps.home.models import MainBanner
from apps.events.models import Event
from apps.gallery.models import GalleryImage
from apps.careers.models import CareerDepartment, CareerRole


# ─────────────────────────────────────────────────────────────────────────────
# HELPER MIXIN
# ─────────────────────────────────────────────────────────────────────────────

class AbsoluteURLMixin:
    def _abs(self, field_file):
        if not field_file:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(field_file.url)
        return field_file.url


# ─────────────────────────────────────────────────────────────────────────────
# HOME — MAIN BANNER
# ─────────────────────────────────────────────────────────────────────────────

class MainBannerSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    image_url        = serializers.SerializerMethodField()
    mobile_image_url = serializers.SerializerMethodField()

    class Meta:
        model  = MainBanner
        fields = [
            'id', 'image_url', 'mobile_image_url',
            'title', 'subtitle', 'cta_label', 'cta_url',
            'display_order', 'is_active',
        ]

    def get_image_url(self, obj):
        return self._abs(obj.image)

    def get_mobile_image_url(self, obj):
        if obj.mobile_image:
            return self._abs(obj.mobile_image)
        return self._abs(obj.image)


# ─────────────────────────────────────────────────────────────────────────────
# EVENTS
# ─────────────────────────────────────────────────────────────────────────────

class EventSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    image_url     = serializers.SerializerMethodField()
    startingPoint = serializers.CharField(source='starting_point', read_only=True)
    destination   = serializers.CharField(read_only=True)
    startdate     = serializers.DateField(source='start_date', read_only=True)
    enddate       = serializers.DateField(source='end_date',   read_only=True)
    infoUrl       = serializers.CharField(source='info_url',   read_only=True)
    is_upcoming   = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Event
        fields = [
            'id', 'title',
            'startingPoint', 'destination',
            'startdate', 'enddate',
            'image_url', 'infoUrl',
            'display_order', 'is_active', 'is_upcoming',
        ]

    def get_image_url(self, obj):
        return self._abs(obj.image)


# ─────────────────────────────────────────────────────────────────────────────
# GALLERY
# ─────────────────────────────────────────────────────────────────────────────

class GalleryImageSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = GalleryImage
        fields = ['id', 'image_url', 'caption', 'display_order', 'is_active']

    def get_image_url(self, obj):
        return self._abs(obj.image)


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────────────────────────────────────

class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductCategory
        fields = ['id', 'name', 'slug', 'display_order', 'is_active']


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductCategory
        fields = ['id', 'name', 'slug', 'display_order', 'is_active']


# ─────────────────────────────────────────────────────────────────────────────
# MOTORCYCLES
# ─────────────────────────────────────────────────────────────────────────────

class ProductColorSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = ProductColor
        fields = ['id', 'name', 'hex', 'image_url', 'price', 'display_order']

    def get_image_url(self, obj):
        return self._abs(obj.image)


class ProductTopAboutSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    top_image_url = serializers.SerializerMethodField()

    class Meta:
        model  = ProductTopAbout
        fields = ['id', 'top_image_url', 'heading', 'description']

    def get_top_image_url(self, obj):
        return self._abs(obj.top_image)


class ProductFeatureSectionSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = ProductFeatureSection
        fields = ['id', 'title', 'description', 'image_url', 'display_order']

    def get_image_url(self, obj):
        return self._abs(obj.image)


class MotorcycleProductListSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    category_name      = serializers.CharField(source='category.name', read_only=True)
    category_slug      = serializers.CharField(source='category.slug', read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    base_price         = serializers.SerializerMethodField()

    class Meta:
        model  = MotorcycleProduct
        fields = [
            'id', 'name', 'slug', 'short_description',
            'featured_image_url', 'engine_cc', 'power', 'torque',
            'base_price', 'category_name', 'category_slug',
            'display_order', 'is_active', 'created_at',
        ]

    def get_featured_image_url(self, obj):
        return self._abs(obj.featured_image)

    def get_base_price(self, obj):
        first = obj.colors.order_by('display_order').first()
        return first.price if first else None


class MotorcycleProductDetailSerializer(AbsoluteURLMixin, serializers.ModelSerializer):
    category           = ProductCategoryListSerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    brochure_url       = serializers.SerializerMethodField()
    top_about          = ProductTopAboutSerializer(read_only=True)
    colors             = ProductColorSerializer(many=True, read_only=True)
    features           = ProductFeatureSectionSerializer(many=True, read_only=True)

    class Meta:
        model  = MotorcycleProduct
        fields = [
            'top_about',
            'id', 'name', 'slug', 'featured_image_url',
            'short_description', 'description',
            'colors',
            'engine_cc', 'power', 'torque',
            'brochure_url',
            'category',
            'features',
            'display_order', 'is_active', 'created_at',
        ]

    def get_featured_image_url(self, obj):
        return self._abs(obj.featured_image)

    def get_brochure_url(self, obj):
        return self._abs(obj.brochure_file)


# ─────────────────────────────────────────────────────────────────────────────
# CAREERS
# ─────────────────────────────────────────────────────────────────────────────

class CareerRoleSerializer(serializers.ModelSerializer):
    whatsapp_url = serializers.SerializerMethodField()

    class Meta:
        model  = CareerRole
        fields = [
            'id',
            'title',
            'whatsapp_url',     # ready-to-use wa.me link for APPLY NOW button
            'display_order',
            'is_active',
        ]

    def get_whatsapp_url(self, obj):
        return obj.get_whatsapp_url()


class CareerDepartmentSerializer(serializers.ModelSerializer):
    roles = CareerRoleSerializer(many=True, read_only=True)

    class Meta:
        model  = CareerDepartment
        fields = [
            'id',
            'name',
            'icon',
            'display_order',
            'is_active',
            'roles',            # all roles nested inside department
        ]