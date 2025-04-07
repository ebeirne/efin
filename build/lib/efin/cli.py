import click
import efin

@click.group()
def cli():
    """Efin: A Financial Analysis Toolkit CLI."""
    pass

@cli.command()
@click.argument("ticker")
@click.option("--model", default="linear", help="Forecast model to use: 'linear' (default) or 'grid'")
@click.option("--period", default=30, help="Number of days to forecast")
@click.option("--start_date", default="2010-01-01", help="Start date for historical data")
def forecast(ticker, model, period, start_date):
    """Forecast stock prices for TICKER."""
    if model.lower() in ["linear", "arima"]:
        # Use the unified forecast function (linear regression based)
        result = efin.forecast(ticker, forecast_period=period, start_date=start_date)
        click.echo(f"Forecast for {ticker}:")
        click.echo(result.to_string(index=False))
    elif model.lower() == "grid":
        # Use grid search ARIMA forecast function
        result, best_order, best_aic = efin.auto_arima_grid_forecast(ticker, forecast_period=period, start_date=start_date)
        click.echo(f"Grid search ARIMA Forecast for {ticker} (best order {best_order}, AIC={best_aic}):")
        click.echo(result.to_string(index=False))
    else:
        click.echo("Unsupported model. Please use 'linear' or 'grid'.")

if __name__ == '__main__':
    cli()
