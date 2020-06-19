#include "mainwindow.h"
#include <iostream>     // temp

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    initializeGUI();
}

MainWindow::~MainWindow()
{
    delete m_splitter;
    delete m_urlBar;
}

void MainWindow::initializeGUI()
{

    m_centralWidget = new QWidget();
    m_layout = new QGridLayout;
    m_centralWidget->setLayout(m_layout);

    m_tabWidget = new QTabWidget();

    /* START Create main content */
    m_splitter = new QSplitter(Qt::Horizontal);
    m_temp_label = new QLabel("Simple Label");
    m_htmlTextBrowser = new QTextBrowser;
    m_splitter->addWidget(m_temp_label);
    m_splitter->addWidget(m_htmlTextBrowser);

    QWidget *dlContainer = createDownloadTab();

    /* END Create main content */

    m_tabWidget->addTab(m_splitter, "Read");
    m_tabWidget->addTab(new QWidget(), "Library");
    m_tabWidget->addTab(dlContainer, "Download Manager");


    m_layout->addWidget(m_tabWidget, 0, 0);
    //setCentralWidget(m_splitter);
    setCentralWidget(m_centralWidget);
    setWindowTitle("ForWantOfANail");
    setMinimumSize(MIN_WIN_WIDTH, MIN_WIN_HEIGHT);

}

QWidget* MainWindow::createDownloadTab()
{
    QWidget *dlContainer = new QWidget;
    QGridLayout *layout = new QGridLayout;
    QPushButton *dlButton = new QPushButton("&Download Fic", this);
    m_urlBar = new QLineEdit();


    dlContainer->setLayout(layout);
    layout->addWidget(m_urlBar, 0, 0, Qt::AlignTop);
    layout->addWidget(dlButton, 0, 1, Qt::AlignTop);

    connect(dlButton, SIGNAL(released()), this, SLOT(handleDownloadButton()));

    return dlContainer;
}

void MainWindow::handleDownloadButton()
{
    m_downloadManager.appendRawFic(m_urlBar->text());
    //m_downloadManager.appendChapter(m_urlBar->text());
}
