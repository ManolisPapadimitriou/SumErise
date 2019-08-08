# IDEddit
Browse Reddit through a dummy IDE.

### Making changes
  * In order to contribute or make changes in general, create an app on reddit and then add your account details to the file ```mypackage/__init__.py``.
  
     How the file should look like
   ```python
     import praw

     handler = praw.Reddit(
     client_id='',
     client_secret='',
     username='',
     password='',
     user_agent=''
     )
   ```
### Credits
  * [PyQT5] (GUI for the program)
  * [PRAW] (wrapper for Reddit API) 
  * [anytree] (helped a lot while parsing comments from posts) 
  * [Class] (Java class that has been used as an example)
  
### Issues to keep in mind
  * The application can break crash easily, if there are a lot of requests. 
  * Some comments won't be displayed due to Reddit API limitations, more info [here] 

[//]: #
   [PyQT5]: <https://github.com/baoboa/pyqt5>
   [PRAW]: <https://github.com/praw-dev/praw>
   [anytree]: <https://github.com/c0fec0de/anytree>
   [here]: <https://github.com/praw-dev/praw/issues/1043#issuecomment-471233284>
   [Class]:                    <https://github.com/openjdk/jdk/blob/master/src/java.desktop/windows/classes/com/sun/java/swing/plaf/windows/AnimationController.java>
