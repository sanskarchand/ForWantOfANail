#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <Qt>
#include <QMainWindow>
#include <QSplitter>
#include <QTabWidget>
#include <QVBoxLayout>
#include <QTextBrowser>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include "Network/DownloadManager.h"

#define MIN_WIN_WIDTH 640
#define MIN_WIN_HEIGHT 480

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void initializeGUI();
    QWidget* createDownloadTab();
private slots:                          //Qt-specific extension for MOC
    void handleDownloadButton();

public:
    DownloadManager m_downloadManager;

    QGridLayout     *m_layout;
    QWidget         *m_centralWidget;
    QTabWidget      *m_tabWidget;
    QSplitter       *m_splitter;
    QTextBrowser    *m_htmlTextBrowser;
    QLabel          *m_temp_label;

    QLineEdit       *m_urlBar;



};
#endif // MAINWINDOW_H
