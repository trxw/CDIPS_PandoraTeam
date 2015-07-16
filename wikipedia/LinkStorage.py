#!/usr/bin/python

UNDESIRABLE_LINKS = [ 
  '/wiki/bibcode',
	'/w/index.php?title=event_(', # These two are to exclude possible  
	################################ direct self-referral since it creates
	################################ an infinite loop while crawling the
	################################ links referred in the html data.
  'digital_object_identifier',
 	'//creativecommons.org/licenses/by-sa/3.0/',
	'/wiki/category:wikipedia_articles_needing',
	'/wiki/category:pages_containing_cite_templates',
	'/wiki/category:featured_articles',
	'/wiki/category:wikipedia_semi-protected_pages',
	'//wikimediafoundation.org/wiki/privacy_policy',
	'/wiki/main_page',
	'//en.wikipedia.org/wiki/wikipedia:contact_us',
	'/wiki/wikipedia:about',
	'/wiki/help:',
	'/wiki/help:',
	'//shop.wikimedia.org',
	'/wiki/special:recentchangeslinked',
	'/wiki/special:booksources/',
	'/wiki/wikipedia:community_portal',
	'/wiki/wikipedia:community_portal',
	'/wiki/category:all_articles_needing_additional_references',
	'//meta.wikimedia.org',
	'/wiki/category:all_articles_lacking_sources',
	'//be-x-old.wikipedia.org/wiki/',
	'//wikimediafoundation.org/wiki/terms_of_use',
	'https://www.mediawiki.org/wiki/special:mylanguage/how_to_contribute',
	'/wiki/Scientific_American',
	'/wiki/Portal:',
	'/wiki/Scientific_American',
	'/wiki/portal:featured_content',
	'/wiki/portal:current_events',
	'/wiki/help:category',
	'/wiki/file:question_book-new.svg',
	'/wiki/wikipedia:file_upload_wizard',
	'/w/index.php?title=special:recentchanges&amp;feed=atom',
	'#p-search',
	'#see_also',
	'/wiki/special:random',
	'/wiki/wikipedia:citing_sources',
	'/wiki/special:recentchanges',
	'//bits.wikimedia.org/apple-touch/wikipedia.png',
	'/wiki/help:introduction_to_referencing/1',
	'/wiki/category:articles_lacking_sources_from_july_2007',
	'//en.wikipedia.org/w/api.php?action=rsd',
	'//www.mediawiki.org/',
	'/wiki/category:wikipedia_indefinitely_move-protected_pages',
	'//en.wikipedia.org/wiki/wikipedia:',
	'https://donate.wikimedia.org/wiki/special:',
	'http://en.wikipedia.org/wiki/template_talk:',
	'/wiki/template_talk:',
	'/wiki/category:articles_with_open_directory_project_links',
	'//en.wikipedia.org/w/index.php?title=template:',
	'http://www.wikidata.org/wiki/',## Note that a link that begins with 
	################################### this refers to the corresponding
	################################### page in which the equivalent of 
	################################### the title of the current page in 
	################################### other languages are listed.
	'//www.wikidata.org/wiki/',
	'/wiki/special:specialpages',
	'/wiki/talk:',
	'//bits.wikimedia.org/en.wikipedia.org/load',
	'/wiki/portal:contents',
	'/w/opensearch_desc.php',
	'//bits.wikimedia.org/favicon/wikipedia.ico',
	'//bits.wikimedia.org',
	'/w/index.php?title=special:book&',
	'/wiki/special:whatlinkshere',
	'/w/index.php?title=special:userlogin',
	'/wiki/oxford_university_press',
	'/wiki/wikipedia:',
	'/wiki/especial:',
	'/wiki/especial%',
	'/wiki/spezial:',
	'/wiki/spezial%',
	'/wiki/special:',
	'/wiki/special%',
	'/wiki/wikipedia_diskussion:',
	'/wiki/spesial:',
	'/wiki/spesial%',
	'/wiki/specjalna:',
	'/wiki/specjalna%',
	'/wiki/speciaal:',
	'/wiki/speciaal%',
	'/wiki/speciel:',
	'/wiki/speciel%',
	'/wiki/category:cs1_errors:_dates',
	'/wiki/category:hidden_templates_using_styles',
	'/wiki/category:wikipedia_indefinitely_semi-protected_pages',
	'/wiki/category:all_articles_with_unsourced_statements',
	'/wiki/category:articles_with_unsourced_statements',
	'/wiki/book:',
	'/w/index.php?title=',
	'#mw-navigation',
	'/wiki/category:articles_containing',
	'/wiki/category:use_dmy_dates_from',
	'/wiki/Digital_object_identifier',
	'/wiki/Bibcode',
	]

# Note that before checking this list, it must be ensured that the link
# is not a bad link, that is it is not in either UNDESIRABLE_LINKS, FILES
# or in BAD_EXTENTIONS.


## IMPORTANT NOTE: This can in fact help a lot in determining important
	##################### subcatagories of each field. For example, /wiki/Category:Mathematics
	##################### has a subcaragory /wiki/Category:Fields_of_Mathematics 
TEMPLATE_OR_CATEGORY = [
	'/wiki/template:',
	'/wiki/category:', 
	'/template:', 
	]

FILES = [
	'/wiki/file:',
	'.jpg',
#	'.JPG', 
	'.png',
#	'.PNG', 
	'.pdf',
#	'.PDF',
	'.svg',
	]	

#Must be entered in lowercase:
BAD_EXTENTIONS = [
 	'digital_object_identifier',
	'edit',
	'printable=yes',
	'#sitelinks-wikipedia',
	'#mw-navigation',
	'wikipedia:general_disclaimer',
	'&amp;action=info',
	'skin=vector&amp;*',
	'&amp;writer=rl',
	'#external_links',
	'#p-search',
	'#a_note_on_notation',
	'#external_links',
	'#notes',
	'#see_also',
	'/wiki/inverse_image',
	'/w/index.',
	'wikipedia.',
	'wikipedia.',
	'wikipedia',
	'/ka.wikipedia.',
	'pedia.',
	'wikimediafoundation.org/',
	'wikimediafoundation.org',
	'/wiki/springer_science%2bbusiness_media',
	'http://en.wikipedia.org/wiki/OCLC',
	'//en.wikipedia.org/wiki/OCLC',
	#'mwl',  	
	#'vec',
	#'csb'
	#'zea'
	#'bat-smg'
	'/wiki/international_standard_book_number',
	'education.aspx',
	'/w/',
	'/trap/',
	]

BOOK_SITE_LIST = [
	"books.google.com/",
	"www.amazon.",
	]

