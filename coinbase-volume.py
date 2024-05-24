import time
import smtplib
from coinbasepro import PublicClient

#
# STRATEGY: 
# access every coin on coinbase.
# Compute the daily EMA 20.
# Notify me when it closes above the EMA 20
#

def send_email(subject, msg, from_email, to_email, password):
    try:
        # Ctrl + / comments the selected lines
        # server = smtplib.SMTP('smtp.gmail.com:587')
        # server.ehlo()
        # server.starttls()
        # server.login(from_email, password)
        # message = 'Subject: {}\n\n{}'.format(subject, msg)
        # server.sendmail(from_email, to_email, message)
        # server.quit()
        # print("Email sent!")
        print("Ignoring email for now")
    except Exception as e:
        print("Failed to send email: ", e)

def monitor_volume(symbol, threshold):
    client = PublicClient()
    last_vol = 0
    while True:
        stats = client.get_product_24hr_stats(symbol)
        volume = float(stats['volume'])
        print(f"Current 24hr trading volume for {symbol}: {volume}. Volume change {volume-last_vol}")
        if volume > threshold:
            send_email("Volume Alert", f"Trading volume for {symbol} exceeded {threshold}", 'Your Email', 'Recipient Email', 'Your Password')
        time.sleep(60)  # wait for 60 seconds before checking again

        last_vol = volume

def volume_oscillator():
    print("from chat gpt to emulate the tradingview 'supertrend volume' indicator")
    # Retrieve historical volume data (replace with actual parameters)
    historical_data = client.get_historical_candles(product_id="BTC-USD", granularity=3600)

    # Calculate Supertrend and direction (replace with actual logic)
    # ...

    # Calculate directionalSum, totalSum, and indicatorValue
    # ...

    # Assign colors and highlight zones (replace with actual logic)
    # ...

    """
    Pinescript reference:

    lookbackPeriod = input.int(300, "Lookback Period")
    supertrendFactor = input.float(3.0, "Supertrend Factor")
    atrPeriod = input.int(12, "Supertrend ATR Period")
    channelThreshold = input.float(50.0, "Overbought/Oversold Levels (absolute value)", minval = 0, maxval = 100, step = 1)
    displayZones = input.bool(true, "Show Overbought/Oversold zones")

    // Check for availability of volume data
    if barstate.islast and ta.cum(volume) == 0
        runtime.error("No volume data available.")

    // Calculating Supertrend and its direction
    [supertrend, direction] = ta.supertrend(supertrendFactor, atrPeriod)

    // Initializing variables for sum calculations
    float directionalSum = 0.0
    float obvSum = 0.0
    float totalSum = 0.0

    // Summation of directional and total volume for the oscillator calculation
    directionalSum := math.sum(-direction * volume, lookbackPeriod)
    totalSum := math.sum(volume, lookbackPeriod)

    // Oscillator value calculation as a ratio of directional to total volume
    float indicatorValue = directionalSum / totalSum * 100

    // Assigning a plot color based on the indicator value relative to the channel threshold
    color plotColor = color.from_gradient(indicatorValue, -channelThreshold, channelThreshold, color.rgb(179, 0, 72), color.rgb(169, 231, 0))

    // Highlighting background based on overbought and oversold conditions
    bool isTopZone    = indicatorValue > channelThreshold and math.sign(direction) < 0
    bool isBottomZone = indicatorValue < -channelThreshold and math.sign(direction) > 0 

    // Fill Colors
    color zoneColor = isTopZone and displayZones ? color.new(color.lime, 60) : isBottomZone and displayZones? color.new(color.red, 60) : na
    color fillColor = color.from_gradient(ta.sma(-direction,12), -1, 1, color.new(color.red,85), color.new(color.yellow,85))

    // Plotting the indicator value
    zeroLine = plot(0,display = display.none)
    filline = plot(isTopZone ? 100 : -100,display = display.none)
    indicatorPlot = plot(indicatorValue, color = plotColor, title="Supertrend Volume Oscillator", linewidth = 3)
    fill(zeroLine,indicatorPlot,fillColor)
    fill(filline,indicatorPlot,zoneColor)

    // Reference lines for neutral, top, and bottom levels
    hline(0, "Zero Line", color=color.gray)
    hline(100, title="Top Line", color=color.green, linestyle=hline.style_dashed)
    hline(-100, title="Bottom Line", color=color.red, linestyle=hline.style_dashed)

    // Alert conditions for entering overbought and oversold zones
    bool enteredTopZone = not(isTopZone[1]) and isTopZone
    bool enteredBottomZone = not(isBottomZone[1]) and isBottomZone

    alertcondition(enteredBottomZone, "Bottom Zone", "Supertrend VOL: {{ticker}} ({{interval}}) Bottom Zone ▲▲ [{{close}}]")
    alertcondition(enteredTopZone, "Top Zone", "Supertrend VOL: {{ticker}} ({{interval}}) Top Zone ▼▼ [{{close}}]")
    
    """

    print("Volume data retrieved and analysis performed.")

if __name__ == "__main__":
    monitor_volume('BTC-USD', 10000)  # monitor Bitcoin trading volume

mv = monitor_volume