from sexpParser import *

######### Test data ###########
test00 = """(snicker "abc" (#03# |YWJj|))"""
test01 = """(certificate
 (issuer
  (name
   (public-key
    rsa-with-md5
    (e |NFGq/E3wh9f4rJIQVXhS|)
    (n |d738/4ghP9rFZ0gAIYZ5q9y6iskDJwASi5rEQpEQq8ZyMZeIZzIAR2I5iGE=|))
   aid-committee))
 (subject
  (ref
   (public-key
    rsa-with-md5
    (e |NFGq/E3wh9f4rJIQVXhS|)
    (n |d738/4ghP9rFZ0gAIYZ5q9y6iskDJwASi5rEQpEQq8ZyMZeIZzIAR2I5iGE=|))
   tom
   mother))
 (not-before "1997-01-01_09:00:00")
 (not-after "1998-01-01_09:00:00")
 (tag
  (spend (account "12345678") (* numeric range "1" "1000"))))
"""
test02 = """(lambda (x) (* x x))"""
test03 = """(def length
   (lambda (x)
      (cond
         ((not x) 0)
         (   t   (+ 1 (length (cdr x))))
      )
   )
)
"""
test04 = """(2:XX "abc" (#30# |YWJj|))"""
test05 = """(if (is (window_name) "XMMS") (set_workspace 2))"""
test06 = """(if
  (and
    (is (application_name) "Firefox")
    (or
      (contains (window_name) "Enter name of file to save to")
      (contains (window_name) "Save As")
      (contains (window_name) "Save Image")
    )
  )
  (geometry "+140+122")
)
"""
test07 = """(defun factorial (x)
   (if (zerop x) 1
       (* x (factorial (- x 1)))))
       """
test51 = """(3:XX "abc" (#30# |YWJj|))"""

# Run tests
t = None
alltests = [ locals()[t] for t in sorted(locals()) if t.startswith("test") ]

for t in alltests:
    print '-'*50
    print t
    try:
        sexpr = sexp.parseString(t)
        pprint.pprint(sexpr.asList())
    except ParseFatalException, pfe:
        print "Error:", pfe.msg
        print line(pfe.loc,t)
        print pfe.markInputline()
    print
