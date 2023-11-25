dest_country_airport_dict = {'Argentina': ['AEP'], 'Australia': ['SYD', 'MEL'], 'Austria': ['VIE'], 'Brazil': ['GRU', 'CNF', 'VCP'], 'Belgium': ['BRU'], 'Canada': ['YYZ'], 'Chile': ['SCL'], 'China': ['CAN', 'SZX', 'PVG', 'SHA', 'HGH', 'CTU', 'XIY', 'CGO', 'PEK'], 'Columbia': ['BOG'], 'Denmark': ['CPH'], 'Dublin': ['DUB'], 'Ethiopia': ['ADD'], 'Egypt': ['CAI'], 'France': ['CDG'], 'Germany': ['MUC', 'FRA'], 'India': ['DEL', 'BOM', 'BLR'], 'Greece': ['ATH'], 'Indonesia': ['CGK'], 'Italy': ['MXP'], 'Japan': ['NRT', 'HND'], 'Kenya': ['NBO'], 'Mexico': ['MEX'], 'Malaysia': ['KUL'], 'Morocco': ['CMN'], 'Norway': ['OSL'], 'Netherlands': ['AMS'], 'Panama': ['PTY'], 'Philippines': ['MNL'], 'Peru': ['LIM'], 'Portugal': ['LIS'], 'Italy': ['FCO'], 'Qatar': ['DOH'], 'Russia': ['SVO', 'DME'], 'Singapore': ['SIN'], 'South Africa': ['JNB', 'CPT'], 'South Korea': ['ICN'], 'Spain': ['MAD'], 'Taiwan': ['TPE'], 'Sweden': ['ARN'], 'Thailand': ['BKK'], 'Turkey': ['SAW', 'IST'], 'United Arab Emirates': ['DXB'], 'United Kingdom': ['LHR', 'LGW', 'MAN'], 'United States': ['ATL', 'ORD', 'LAX', 'PHX', 'MCO', 'CLT', 'MIA', 'IAH', 'SEA', 'FLL', 'SFO', 'JFK'], 'Zurich': ['ZRH'], 'Algeria': ['ALG'], 'Vietnam': ['SGN']}

from_country_airport_dict = {'Algeria': ['ALG'], 'Argentina': ['AEP'], 'Australia': ['SYD', 'MEL'], 'Austria': ['VIE'], 'Belgium': ['BRU'], 'Brazil': ['GRU', 'CNF', 'VCP'], 'Canada': ['YYZ'], 'Chile': ['SCL'], 'China': ['CAN', 'CTU', 'SZX', 'PEK', 'SHA', 'XIY', 'PVG', 'HGH', 'CGO'], 'Columbia': ['BOG'], 'Denmark': ['CPH'], 'Dublin': ['DUB'], 'Egypt': ['CAI'], 'Ethiopia': ['ADD'], 'France': ['CDG'], 'Germany': ['FRA', 'MUC'], 'Greece': ['ATH'], 'India': ['DEL', 'BOM']}

airport_to_country = {
    'AEP': 'Argentina', 'SYD': 'Australia', 'MEL': 'Australia', 'VIE': 'Austria', 
    'GRU': 'Brazil', 'CNF': 'Brazil', 'VCP': 'Brazil', 'BRU': 'Belgium', 'YYZ': 'Canada', 
    'SCL': 'Chile', 'CAN': 'China', 'SZX': 'China', 'PVG': 'China', 'SHA': 'China', 
    'HGH': 'China', 'CTU': 'China', 'XIY': 'China', 'CGO': 'China', 'PEK': 'China', 
    'BOG': 'Columbia', 'CPH': 'Denmark', 'DUB': 'Dublin', 'ADD': 'Ethiopia', 'CAI': 'Egypt', 
    'CDG': 'France', 'MUC': 'Germany', 'FRA': 'Germany', 'DEL': 'India', 'BOM': 'India', 
    'BLR': 'India', 'ATH': 'Greece', 'CGK': 'Indonesia', 'MXP': 'Italy', 'NRT': 'Japan', 
    'HND': 'Japan', 'NBO': 'Kenya', 'MEX': 'Mexico', 'KUL': 'Malaysia', 'CMN': 'Morocco', 
    'OSL': 'Norway', 'AMS': 'Netherlands', 'PTY': 'Panama', 'MNL': 'Philippines', 
    'LIM': 'Peru', 'LIS': 'Portugal', 'FCO': 'Italy', 'DOH': 'Qatar', 'SVO': 'Russia', 
    'DME': 'Russia', 'SIN': 'Singapore', 'JNB': 'South Africa', 'CPT': 'South Africa', 
    'ICN': 'South Korea', 'MAD': 'Spain', 'TPE': 'Taiwan', 'ARN': 'Sweden', 'BKK': 'Thailand', 
    'SAW': 'Turkey', 'IST': 'Turkey', 'DXB': 'United Arab Emirates', 'LHR': 'United Kingdom', 
    'LGW': 'United Kingdom', 'MAN': 'United Kingdom', 'ATL': 'United States', 
    'ORD': 'United States', 'LAX': 'United States', 'PHX': 'United States', 'MCO': 'United States', 
    'CLT': 'United States', 'MIA': 'United States', 'IAH': 'United States', 'SEA': 'United States', 
    'FLL': 'United States', 'SFO': 'United States', 'JFK': 'United States', 'ZRH': 'Zurich', 
    'ALG': 'Algeria', 'SGN': 'Vietnam'
}
