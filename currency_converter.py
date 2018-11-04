"""
Currency Conversion Discord Bot

This bot converts between world currencies.
The conversion information is gathered from here: https://free.currencyconverterapi.com/
The source code can be found here: https://github.com/Mamba-Bajamba/discord-currency-converter

Author: Hamish Croser
Created: 31-10-2018
Edited: 05-11-2018
Version: 2.0
"""

from lxml import html
import requests
import time
import os
import discord
from discord.ext import commands

#Check for config.py file
if os.path.isfile("config.py"):
    import config
else:
    sys.exit("'config.py' is required. Please add it and try again.")

# Discord Bot Construction
TOKEN = config.bot_token
client = commands.Bot(command_prefix=config.cmd_prefix)

# Help command is re-written further down
client.remove_command('help')


@client.command(pass_context=True)
async def convert(ctx, *args):
    await client.send_typing(ctx.message.channel)

    # Function that requests conversion rate
    def conversionProcess(initCurrency,finalCurrency,initValue):
        URL = 'https://free.currencyconverterapi.com/api/v6/convert?q={}_{}&compact=ultra'.format(initCurrency,finalCurrency)
        page = requests.get(URL)
        raw = page.text

        conversionRate = float(raw[11:-2])
        finalValue = round(conversionRate*initValue, 2)
        conversionRate = round(conversionRate, 2)

        output = '**{0:.2f}{1}** is equal to **{2}{3}**\nThe conversion rate is **1.00{1} = {4}{3}**'.format(initValue,initCurrency,finalValue,finalCurrency,conversionRate)

        return output

    # Performs various checks to ensure user-entered data is of a known format
    def inputCheck(currency1,currency2,initValue):
        # Check that codes are within the dictionary
        if (currency1 in values) and (currency2 in values):
            initCurr = currency1
            finalCurr = currency2

            validInput = True
            # Ensure that values entered are values and not keys
            try:
                testCode = countryToCurrency[currency1]
                validInput = False
            except KeyError:
                validInput = True
                try:
                    testCode = countryToCurrency[currency2]
                    validInput = False
                except KeyError:
                    validInput = True

            # Test for no amount input or invalid amount input
            try:
                initVal = round(float(initValue), 2)
            except ValueError:
                validInput = False

            if validInput:
                output = conversionProcess(initCurr,finalCurr,initVal)
            else:
                output = err_msg
        else:
            output = err_msg

        return output


    # If the user simply calls 'convert', default currency and init_val apply
    if (len(args) == 0):
        initCurr = config.defaultInitCurr
        finalCurr = config.defaultFinalCurr
        initVal = 1.00

        output = conversionProcess(initCurr,finalCurr,initVal)

    # If the user omits the amount value, it defaults to 1.00
    elif (len(args) == 2):
        initVal = 1.00
        output = inputCheck(args[0],args[1],initVal)

    # Regular input with init_curr,final_curr,init_val
    elif (len(args) == 3):
        output = inputCheck(args[0],args[1],args[2])

    # If input is longer than expected, it is treated as an unknown input
    else:
        output = config.err_msg

    await client.say(output)

@client.command(pass_context=True)
async def setdefault(ctx, *args):
    await client.send_typing(ctx.message.channel)

    if (len(args) != 2):
        output = config.err_msg

    elif (args[1] in values) and (args[1] in values):
        with open("config.py", "r") as f:
            fileList = f.readlines()

            for idx,line in enumerate(fileList):
                if line.startswith("defaultInitCurr"):
                    fileList[idx] = "defaultInitCurr = '{}'\n".format(args[0])

                elif line.startswith("defaultFinalCurr"):
                    fileList[idx] = "defaultFinalCurr = '{}'\n".format(args[1])

        with open("config.py", "w") as f:
            f.writelines(fileList)

        output = 'The new default conversion is {0} to {1}'.format(config.defaultInitCurr,config.defaultFinalCurr)
    else:
        output = config.err_msg

    await client.say(output)

@client.command(pass_context=True)
async def code(ctx, *args):
    await client.send_typing(ctx.message.channel)

    if (len(args) == 0):
        output = err_msg
    else:
        try:
            code = countryToCurrency[" ".join(args).capitalize()]
            output = 'The code for {} is {}'.format(args[0],code)
        except KeyError:
            output = err_msg

    await client.say(output)

@client.command(pass_context=True)
async def help(ctx, *args):

    output = 'This bot converts currency values. The bot may be called with `{0}` followed by one of these commands:\n\t- `help`: displays this message\n\t- `list`: lists all of the countries and their respective codes\n\t- `code `*`country-name`*: sends the code of the country\n\t- `setdefault `*`initial-currency converted-currency`*: sets the default conversion to *initial-currency* to *converted-currency*\n\t- `convert`: The format of a conversion request is: *`currency-to-convert-code converted-currency-code amount-to-convert`*\nAn example:\n`{0}convert USD AUD 50`\nIf only `{0}` is entered, the default conversion will be 1{1} to {2}.'.format(config.cmd_prefix,config.defaultInitCurr,config.defaultFinalCurr)

    await client.say(output)

@client.command(pass_context=True)
async def list(ctx, *args):

    output = 'This is a list of all countries and their respective code:\n\n'
    for keyValue in countryToCurrency:
        output += '{}: {}, '.format(keyValue,countryToCurrency[keyValue])

    # Output must be split to account for Discord's 2000 character limit. Specific values are to maintain formatting
    outputList = [output[:1372], output[1372:2744], output[2744:-2]]

    for i in range(3):
        await client.say(outputList[i])

@client.command(pass_context=True)
async def thesenate(ctx, *args):

    output = "**Did you ever hear the tragedy of Darth Plagueis the Wise? I thought not. It's not a story the Jedi would tell you. It's a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic, he could save others from death, but not himself.** \n\nhttps://imgur.com/8KPtRjS"

    await client.say(output)


# Dictionary of all countries and their respective currencies
countryToCurrency = {'Afghanistan': 'AFN', 'Akrotiri and Dhekelia': 'EUR', 'Aland Islands': 'EUR', 'Albania': 'ALL', 'Algeria': 'DZD', 'American Samoa': 'USD', 'Andorra': 'EUR', 'Angola': 'AOA', 'Anguilla': 'XCD', 'Antigua and Barbuda': 'XCD', 'Argentina': 'ARS', 'Armenia': 'AMD', 'Aruba': 'AWG', 'Ascension Island': 'SHP', 'Australia': 'AUD', 'Austria': 'EUR', 'Azerbaijan': 'AZN', 'Bahamas': 'BSD', 'Bahrain': 'BHD', 'Bangladesh': 'BDT', 'Barbados': 'BBD', 'Belarus': 'BYN', 'Belgium': 'EUR', 'Belize': 'BZD', 'Benin': 'XOF', 'Bermuda': 'BMD', 'Bhutan': 'BTN', 'Bolivia': 'BOB', 'Bonaire': 'USD', 'Bosnia and Herzegovina': 'BAM', 'Botswana': 'BWP', 'Brazil': 'BRL', 'British Indian Ocean Territory': 'USD', 'British Virgin Islands': 'USD', 'Brunei': 'BND', 'Bulgaria': 'BGN', 'Burkina Faso': 'XOF', 'Burundi': 'BIF', 'Cabo Verde': 'CVE', 'Cambodia': 'KHR', 'Cameroon': 'XAF', 'Canada': 'CAD', 'Caribbean Netherlands': 'USD', 'Cayman Islands': 'KYD', 'Central African Republic': 'XAF', 'Chad': 'XAF', 'Chatham Islands': 'NZD', 'Chile': 'CLP', 'China': 'CNY', 'Christmas Island': 'AUD', 'Cocos Islands': 'AUD', 'Colombia': 'COP', 'Comoros': 'KMF', 'Congo, Democratic Republic of the': 'CDF', 'Republic of the Congo': 'XAF', 'Costa Rica': 'CRC', "Cote d'Ivoire": 'XOF', 'Croatia': 'HRK', 'Cuba': 'CUP', 'Curacao': 'ANG', 'Cyprus': 'EUR', 'Czech Republic': 'CZK', 'Denmark': 'DKK', 'Djibouti': 'DJF', 'Dominica': 'XCD', 'Dominican Republic': 'DOP', 'Ecuador': 'USD', 'Egypt': 'EGP', 'El Salvador': 'USD', 'Equatorial Guinea': 'XAF', 'Eritrea': 'ERN', 'Estonia': 'EUR', 'Eswatini': 'SZL', 'Ethiopia': 'ETB', 'Falkland Islands': 'FKP', 'Fiji': 'FJD', 'Finland': 'EUR', 'France': 'EUR', 'French Guiana': 'EUR', 'French Polynesia': 'XPF', 'Gabon': 'XAF', 'Gambia': 'GMD', 'Georgia': 'GEL', 'Germany': 'EUR', 'Ghana': 'GHS', 'Gibraltar': 'GIP', 'Greece': 'EUR', 'Greenland': 'DKK', 'Grenada': 'XCD', 'Guadeloupe': 'EUR', 'Guam': 'USD', 'Guatemala': 'GTQ', 'Guernsey': 'GGP', 'Guinea': 'GNF', 'Guinea-Bissau': 'XOF', 'Guyana': 'GYD', 'Haiti': 'HTG', 'Honduras': 'HNL', 'Hong Kong': 'HKD', 'Hungary': 'HUF', 'Iceland': 'ISK', 'India': 'INR', 'Indonesia': 'IDR', 'International Monetary Fund': 'XDR', 'Iran': 'IRR', 'Iraq': 'IQD', 'Ireland': 'EUR', 'Isle of Man': 'IMP', 'Israel': 'ILS', 'Italy': 'EUR', 'Jamaica': 'JMD', 'Japan': 'JPY', 'Jersey': 'JEP', 'Jordan': 'JOD', 'Kazakhstan': 'KZT', 'Kenya': 'KES', 'Kiribati': 'AUD', 'Kosovo': 'EUR', 'Kuwait': 'KWD', 'Kyrgyzstan': 'KGS', 'Laos': 'LAK', 'Latvia': 'EUR', 'Lebanon': 'LBP', 'Lesotho': 'LSL', 'Liberia': 'LRD', 'Libya': 'LYD', 'Liechtenstein': 'CHF', 'Lithuania': 'EUR', 'Luxembourg': 'EUR', 'Macau': 'MOP', 'Macedonia': 'MKD', 'Madagascar': 'MGA', 'Malawi': 'MWK', 'Malaysia': 'MYR', 'Maldives': 'MVR', 'Mali': 'XOF', 'Malta': 'EUR', 'Marshall Islands': 'USD', 'Martinique': 'EUR', 'Mauritania': 'MRU', 'Mauritius': 'MUR', 'Mayotte': 'EUR', 'Mexico': 'MXN', 'Micronesia': 'USD', 'Moldova': 'MDL', 'Monaco': 'EUR', 'Mongolia': 'MNT', 'Montenegro': 'EUR', 'Montserrat': 'XCD', 'Morocco': 'MAD', 'Mozambique': 'MZN', 'Myanmar': 'MMK', 'Namibia': 'NAD', 'Nauru': 'AUD', 'Nepal': 'NPR', 'Netherlands': 'EUR', 'New Caledonia': 'XPF', 'New Zealand': 'NZD', 'Nicaragua': 'NIO', 'Niger': 'XOF', 'Nigeria': 'NGN', 'Niue': 'NZD', 'Norfolk Island': 'AUD', 'Northern Mariana Islands': 'USD', 'North Korea': 'KPW', 'Norway': 'NOK', 'Oman': 'OMR', 'Pakistan': 'PKR', 'Palau': 'USD', 'Palestine': 'ILS', 'Panama': 'USD', 'Papua New Guinea': 'PGK', 'Paraguay': 'PYG', 'Peru': 'PEN', 'Philippines': 'PHP', 'Pitcairn Islands': 'NZD', 'Poland': 'PLN', 'Portugal': 'EUR', 'Puerto Rico': 'USD', 'Qatar': 'QAR', 'Reunion': 'EUR', 'Romania': 'RON', 'Russia': 'RUB', 'Rwanda': 'RWF', 'Saba': 'USD', 'Saint Barthelemy': 'EUR', 'Saint Helena': 'SHP', 'Saint Kitts and Nevis': 'XCD', 'Saint Lucia': 'XCD', 'Saint Martin': 'EUR', 'Saint Pierre and Miquelon': 'EUR', 'Saint Vincent and the Grenadines': 'XCD', 'Samoa': 'WST', 'San Marino': 'EUR', 'Sao Tome and Principe': 'STN', 'Saudi Arabia': 'SAR', 'Senegal': 'XOF', 'Serbia': 'RSD', 'Seychelles': 'SCR', 'Sierra Leone': 'SLL', 'Singapore': 'SGD', 'Sint Eustatius': 'USD', 'Sint Maarten': 'ANG', 'Slovakia': 'EUR', 'Slovenia': 'EUR', 'Solomon Islands': 'SBD', 'Somalia': 'SOS', 'South Africa': 'ZAR', 'South Georgia Island': 'GBP', 'South Korea': 'KRW', 'South Sudan': 'SSP', 'Spain': 'EUR', 'Sri Lanka': 'LKR', 'Sudan': 'SDG', 'Suriname': 'SRD', 'Svalbard and Jan Mayen': 'NOK', 'Sweden': 'SEK', 'Switzerland': 'CHF', 'Syria': 'SYP', 'Taiwan': 'TWD', 'Tajikistan': 'TJS', 'Tanzania': 'TZS', 'Thailand': 'THB', 'Timor-Leste': 'USD', 'Togo': 'XOF', 'Tokelau': 'NZD', 'Tonga': 'TOP', 'Trinidad and Tobago': 'TTD', 'Tristan da Cunha': 'GBP', 'Tunisia': 'TND', 'Turkey': 'TRY', 'Turkmenistan': 'TMT', 'Turks and Caicos Islands': 'USD', 'Tuvalu': 'AUD', 'Uganda': 'UGX', 'Ukraine': 'UAH', 'United Arab Emirates': 'AED', 'United Kingdom': 'GBP', 'United States of America': 'USD', 'Uruguay': 'UYU', 'US Virgin Islands': 'USD', 'Uzbekistan': 'UZS', 'Vanuatu': 'VUV', 'Vatican City': 'EUR', 'Venezuela': 'VEF', 'Vietnam': 'VND', 'Wake Island': 'USD', 'Wallis and Futuna': 'XPF', 'Yemen': 'YER', 'Zambia': 'ZMW', 'Zimbabwe': 'USD'}

values = countryToCurrency.values()

client.run(TOKEN)
