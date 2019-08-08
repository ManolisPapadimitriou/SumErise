import sys
from PyQt5.QtWidgets import *
from finalDesign import *
from reddit import *
from comment_handler import *
from anytree.exporter import JsonExporter, DictExporter

class MainWindow(QtWidgets.QMainWindow):
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_init_data()
        self.ui.subreddit.returnPressed.connect(self.load_subreddit)
        self.ui.postUrl.setReadOnly(True)
        self.ui.postBody.setReadOnly(True)
        self.ui.postTitle.setReadOnly(True)
        self.ui.redditList.itemDoubleClicked.connect(self.clicked)

    def set_init_data(self):
        self.load_popular_sub()

    def load_popular_sub(self):
        global posts
        posts = Reddit.call_posts("testingground4bots")

        counter = 0
        for post in posts:
            counter = counter + 1
            self.ui.redditList.addItem(
                Comment_Handler.list_item_format(counter, post.score, post.title, post.url, post.subreddit,post.number_of_comments)
            )

    def load_subreddit(self):
        self.ui.redditList.clear()
        if not self.ui.subreddit.text() == "":
            #flag will be used on whether we need to print the subreddit name
            flag = False
            sub_name = ""
            # /r/all is similar with /r/popular, we need the subreddit name as well
            if self.ui.subreddit.text() == "all":
                flag = 1
            elif self.ui.subreddit.text() == "popular":
                flag = 2
            counter = 0;
            global posts
            posts = Reddit.call_posts(self.ui.subreddit.text())
            # check if given subreddit exists
            if posts:
                self.ui.messageLabel.setText("")
                for post in posts:
                    counter = counter + 1
                    if flag:
                        sub_name = post.subreddit
                    self.ui.redditList.addItem(
                        Comment_Handler.list_item_format(counter, post.score, post.title, post.url, sub_name, post.number_of_comments)
                    )
                if flag == 1:
                    self.ui.subredditTitle.setText("/All")
                elif flag == 2:
                    self.ui.subredditTitle.setText("/Popular")
                else:
                    self.ui.subredditTitle.setText(post.subreddit)
            else:
                self.ui.messageLabel.setText("Wrong subreddit name!")
                self.ui.subredditTitle.setText("Subreddit not found! ")
            self.ui.subreddit.setText("")

    def iterate_dict(self, dict_comments, l):
        for p_id, p_info in dict_comments.items():
            if isinstance(p_info, list):
                l_child = QTreeWidgetItem(["EMPTY_CHILD"])
                # print("\nCHILDREN: " + format(p_id) + "\t HAS " + format(len(p_info)) + " children")
                #Loop list with children -> dict
                for child_dict in p_info:
                    # print("OUTSIDE " + format(child_dict))

                    for child_id, child_info in child_dict.items():
                        if isinstance(child_info, list):
                            # Loop list with children -> dict
                            #TODO limit children (possibly not what we need)
                            counter = 5
                            for grand_dict in child_info:
                                if counter > 0:
                                    # print("Grand: " + format(grand_dict))
                                    l_child.addChild(self.iterate_dict(grand_dict, l_child))
                                    counter = counter - 1
                        else:
                            #add new line every 100 characters
                            if len(child_info) > 140:
                                child_info_split = child_info.split()
                                child_final = ""
                                tmp_str = ""
                                counter = 0
                                for inner in child_info_split:
                                    if counter <= 70:
                                        child_final = child_final + " " + inner
                                        tmp_str = tmp_str + " " + inner
                                        counter = len(tmp_str)
                                    else:
                                        counter = 0
                                        tmp_str = ""
                                        child_final = child_final + "\n"
                                child_info = child_final

                            l_child = QTreeWidgetItem([child_info])
                            l.addChild(l_child)

            else:
                if len(p_info) > 100:
                    p_info_split = p_info.split()
                    p_final = ""
                    tmp_str = ""
                    counter = 0
                    for inner in p_info_split:
                        if counter <= 70:
                            p_final = p_final + " " + inner
                            tmp_str = tmp_str + " " + inner
                            counter = len(tmp_str)
                        else:
                            counter = 0
                            tmp_str = ""
                            p_final = p_final + "\n"
                    p_info = p_final
                l = QTreeWidgetItem([p_info])

        return l




    def clicked(self, item):
        #Getting the index from the counter
        splitted_item_info = item.text().split(" ")
        index = int(splitted_item_info[0]) - 1
        post = posts[index]
        self.ui.postTitle.setText(post.title)
        self.ui.postBody.setText(post.body)
        self.ui.postUrl.setText(post.url)
        self.ui.postSub.setText(post.subreddit)

        #create comments parents and children
        self.ui.treeComments.clear() #clear previous comments
        commentsTree = Reddit.load_comments(post.id)
        # for pre, fill, node in RenderTree(commentsTree):
        #     print("%s%s" % (pre, node.name))
        exporter = JsonExporter(indent=1, sort_keys=False)
        # print(exporter.export(commentsTree))
        dict_exporter = DictExporter()
        dict_comments = dict_exporter.export(commentsTree)
        # print(dict_comments)

        self.ui.treeComments.clear()
        self.ui.treeComments.setStyleSheet("""
                                        QTreeWidget::item {
                                          padding: 20px 0;
                                          border-bottom: 1px solid black;
                                          max-width: 75ch;
                                          
                                        }
                                        QTreeWidget::item:hover {
                                          background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                                          border: 1px solid #bfcde4;
                                        }
                                        QTreeWidget::item:selected  {
                                            color: black;
                                          border-left: 6px solid blue;
                                          background: #6dadd1;
                                        }
                                        
                                        QListWidget::item  {
                                            background-color: red;
                                        }
                                        QLayout::SetNoConstraint

                                        """)

        self.ui.treeComments.addTopLevelItem(self.iterate_dict(dict_comments, QTreeWidgetItem(["EMPTY"])))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.setFixedSize(w.size())
    w.show()
    sys.exit(app.exec_())
