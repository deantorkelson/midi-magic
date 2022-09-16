# this fetches the instruments and their patch numbers from a table I found online
# works pretty good, data just needs a little massaging after due to strange formatting on the website
require 'open-uri'
require 'net/http'
require 'nokogiri'
require 'json'

url = "https://pjb.com.au/muscript/gm.html"
uri = URI.parse(url)

response = Net::HTTP.get_response(uri)
html = response.body
doc = Nokogiri::HTML(html)
table = doc.css("table")[1].text.split("\n").select{|elem| elem.length > 0}
instruments = {}
table.each do |row|
  parsed_row = row.split(' ', 2)
  break if parsed_row.nil?
  patch_number = parsed_row[0]&.strip&.to_i
  instrument = parsed_row[1]&.strip&.downcase&.gsub(' ', '_')
  instruments[instrument] = patch_number
end
json = JSON.generate(instruments.sort_by {|_key, value| value}.to_h)
File.open('instruments.json', 'w') { |file| file.write(json) }
