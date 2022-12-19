from rest_framework import serializers

from investments.models import Portfolio, PortfolioBacktestData


class PortfolioBacktestDataSerializer(serializers.ModelSerializer):
    """
    PortfolioBacktestData serializer
    """

    class Meta:
        """
        Meta
        """

        model = PortfolioBacktestData
        fields = (
            "cagr",
            "max_drawdown",
            "sharpe",
            "standard_deviation",
            "start_date",
        )


class PortfolioSerializer(serializers.ModelSerializer):
    """
    Portfolio serializer
    """
    backtest_data = PortfolioBacktestDataSerializer()

    class Meta:
        """
        Meta
        """

        model = Portfolio
        fields = (
            "name",
            "visible",
            "backtest_data",
        )
