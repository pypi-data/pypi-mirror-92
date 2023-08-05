
from time import time

from nseta.strategy.strategy import *
from nseta.common.history import *
from nseta.common.log import tracelog, default_logger
from nseta.cli.inputs import *
from nseta.archives.archiver import *
from nseta.strategy.strategyManager import *

import click
from datetime import datetime

__all__ = ['test_trading_strategy', 'forecast_strategy', 'scan_trading_strategy']

STRATEGY_MAPPING_KEYS = list(STRATEGY_MAPPING.keys()) + ['custom']

@click.command(help='Measure the performance of your trading strategy')
@click.option('--symbol', '-S',  help='Security code')
@click.option('--start', '-s', help='Start date in yyyy-mm-dd format')
@click.option('--end', '-e', help='End date in yyyy-mm-dd format')
@click.option('--strategy', default='rsi', type=click.Choice(STRATEGY_MAPPING_KEYS),
	help=', '.join(STRATEGY_MAPPING_KEYS) + ". Choose one.")
@click.option('--upper', '-u', default=75, type=float, help='Used as upper limit, for example, for RSI. Only when strategy is "custom", we buy the security when the predicted next day return is > +{upper} %')
@click.option('--lower', '-l', default=25, type=float, help='Used as lower limit, for example, for RSI. Only when strategy is "custom", we sell the security when the predicted next day return is < -{lower} %')
@click.option('--clear', '-c', default=False, is_flag=True, help='Clears the cached data for the given options.')
@click.option('--plot', '-p', default=False, is_flag=True, help='By default(False). --plot, if you would like the results to be plotted.')
@click.option('--intraday', '-i', is_flag=True, help='Test trading strategy for the current intraday price history (Optional)')
@tracelog
def test_trading_strategy(symbol, start, end, strategy, upper, lower, clear, plot, intraday=False):
	if not intraday:
		if not validate_inputs(start, end, symbol, strategy):
			print_help_msg(test_trading_strategy)
			return
		sd = datetime.strptime(start, "%Y-%m-%d").date()
		ed = datetime.strptime(end, "%Y-%m-%d").date()
	start_time = time()
	try:
		clear_cache(clear, intraday)
		sm = strategyManager()
		if intraday:
			sm.test_intraday_trading_strategy(symbol, strategy, lower, upper, plot=True)
		else:
			sm.test_historical_trading_strategy(symbol, sd, ed, strategy, lower, upper, plot=True)
		end_time = time()
		time_spent = end_time-start_time
		print("\nThis run of testing trading strategy took {:.1f} sec".format(time_spent))
	except Exception as e:
		default_logger().debug(e, exc_info=True)
		click.secho('Failed to test trading strategy. Please check the inputs.', fg='red', nl=True)
		return
	except SystemExit:
		pass

@click.command(help='Test/Measure the performance of your trading strategy for multiple stocks')
@click.option('--symbol', '-S',  help='Comma separated security codes. Skip/Leave empty for scanning all stocks in stocks.py.')
@click.option('--start', '-s', help='Start date in yyyy-mm-dd format')
@click.option('--end', '-e', help='End date in yyyy-mm-dd format')
@click.option('--strategy', help=', '.join(STRATEGY_MAPPING_KEYS) + ". Choose one. Leavy empty for scanning through all strategies.")
@click.option('--upper', '-u', default=75, help='Used as upper limit, for example, for RSI. Only when strategy is "custom", we buy the security when the predicted next day return is > +{upper} %')
@click.option('--lower', '-l', default=25, help='Used as lower limit, for example, for RSI. Only when strategy is "custom", we sell the security when the predicted next day return is < -{lower} %')
@click.option('--clear', '-c', default=False, is_flag=True, help='Clears the cached data for the given options.')
@click.option('--intraday', '-i', is_flag=True, help='Test trading strategy for the current intraday price history (Optional)')
@click.option('--orderby', '-o', default='recommendation', type=click.Choice(['symbol','recommendation']),
	help='symbol or recommendation. Choose one. Default is orderby recommendation.')
@tracelog
def scan_trading_strategy(symbol, start, end, strategy, upper, lower, clear, orderby, intraday=False):
	if not intraday:
		if not validate_inputs(start, end, symbol, None, skip_symbol=True):
			print_help_msg(test_trading_strategy)
			return
	start_time = time()
	try:
		clear_cache(clear, intraday)
		sm = strategyManager()
		full_summary= sm.scan_trading_strategy(symbol, start, end, strategy, upper, lower, clear, orderby, intraday)
		end_time = time()
		time_spent = end_time-start_time
		print("\nThis run of trading strategy scan took {:.1f} sec".format(time_spent))
		if full_summary is not None and len(full_summary) > 0:
			full_summary= full_summary.dropna()
			if orderby == 'recommendation':
				full_summary = full_summary.sort_values(by='Recommendation',ascending=True)
			print("\n{}\n".format(full_summary.to_string(index=False)))
	except Exception as e:
		default_logger().debug(e, exc_info=True)
		click.secho('Failed to test trading strategy. Please check the inputs.', fg='red', nl=True)
		return
	except SystemExit:
		pass

@click.command(help='Forecast & measure performance of a trading model')
@click.option('--symbol', '-S',  help='Security code')
@click.option('--start', '-s', help='Start date in yyyy-mm-dd format')
@click.option('--end', '-e', help='End date in yyyy-mm-dd format')
@click.option('--strategy', default='rsi', type=click.Choice(STRATEGY_MAPPING_KEYS), 
	help=', '.join(STRATEGY_MAPPING_KEYS) + ". Choose one.")
@click.option('--upper', '-u', default=1.5, help='Only when strategy is "custom". We buy the security when the predicted next day return is > +{upper} %')
@click.option('--lower', '-l', default=1.5, help='Only when strategy is "custom". We sell the security when the predicted next day return is < -{lower} %')
@click.option('--clear', '-c', default=False, is_flag=True, help='Clears the cached data for the given options.')
@click.option('--plot', '-p', default=False, is_flag=True, help='By default(False). --plot, if you would like the results to be plotted.')
@tracelog
def forecast_strategy(symbol, start, end, strategy, upper, lower, clear, plot):
	if not validate_inputs(start, end, symbol, strategy):
		print_help_msg(forecast_strategy)
		return
	sd = datetime.strptime(start, "%Y-%m-%d").date()
	ed = datetime.strptime(end, "%Y-%m-%d").date()
	try:
		clear_cache(clear)
		sm = strategyManager()
		df = sm.get_historical_dataframe(symbol, sd, ed)
		df = sm.prepare_for_historical_strategy(df, symbol)
		plt, result = daily_forecast(df, symbol, strategy, upper_limit=float(upper), lower_limit=float(lower), periods=7, plot=plot)
		if plt is not None:
			plt.show()
	except Exception as e:
		default_logger().debug(e, exc_info=True)
		click.secho('Failed to forecast trading strategy. Please check the inputs.', fg='red', nl=True)
		return
	except SystemExit:
		pass

def clear_cache(clear, intraday=False):
	if clear:
		arch = archiver()
		arch.clearcache(response_type=ResponseType.Intraday if intraday else ResponseType.History, force_clear=True)
