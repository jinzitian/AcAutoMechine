==========
AC Auto Mechine
==========

A fast Python implementation of ac auto mechine


Quickstart
==========
To create band 2 row 6 hashes for input data of 8 dimensions:

.. code-block:: python

    from ac_auto_mechine import Ac_mechine
    
    ### usage one:
    actree = Ac_mechine()
    actree.add_keys('he')
    actree.add_keys('her')
    actree.add_keys('here')
    actree.build_actree()
    ### 完全匹配
    print(actree.match("he here her"))  
    ### 最长匹配
    print(actree.match_long("he here her"))  
    ### 完全匹配 显示查找路径
    print(actree.match("he here her"), True)  
    ### 最长匹配 显示查找路径
    print(actree.match_long("he here her"), True)  
    
	
