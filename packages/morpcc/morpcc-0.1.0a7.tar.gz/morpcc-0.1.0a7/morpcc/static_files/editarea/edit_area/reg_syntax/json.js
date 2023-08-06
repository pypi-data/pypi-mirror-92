/**
 * JSON Syntax v0.1
 * 
 * v0.1 by Izhar Firdaus (2020/04/10)
 *   
**/
editAreaLoader.load_syntax["json"] = {
	'DISPLAY_NAME' : 'JSON'
	,'COMMENT_SINGLE' : {1: '//'}
	,'COMMENT_MULTI' : {'/*': '*/'}
	,'QUOTEMARKS' : {1: '"'}
	,'KEYWORD_CASE_SENSITIVE' : true
	,'KEYWORDS' : {	}
	,'OPERATORS' :[
	]
	,'DELIMITERS' :[
          '[', ']', '{', '}'
	]
	,'STYLES' : {
		'COMMENTS': 'color: #AAAAAA;'
		,'QUOTESMARKS': 'color: #660066;'
		,'KEYWORDS' : {}
		,'OPERATORS' : 'color: #993300;'
		,'DELIMITERS' : 'color: #993300;'
			
	}
};
