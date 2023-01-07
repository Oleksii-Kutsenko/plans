from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from accounts.models import User
from countries.models import Country


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    birth_date = serializers.DateField(required=True)
    country = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Country.objects.all()
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "birth_date",
            "country",
            "username",
            "password",
            "password2",
        )

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data: dict) -> User:
        user = User.objects.create(
            birth_date=validated_data["birth_date"],
            country_id=validated_data["country"].id,
            username=validated_data["username"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
