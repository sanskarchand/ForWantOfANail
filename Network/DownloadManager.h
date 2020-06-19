#ifndef DOWNLOADMANAGER_H
#define DOWNLOADMANAGER_H

#include "utils.h"

#include <QtCore>
#include <QtNetwork/QtNetwork>
#include <QtNetwork/QNetworkRequest>
#include <QtNetwork/QNetworkReply>


struct FicDownloadData
{
    FicDownloadData(int chapters, std::string baseURL)
        : numChaps(chapters), baseURL(baseURL) {}

    int numChaps;
    std::string baseURL;
    int downloaded = 0;
};

class DownloadManager : public QObject
{
    Q_OBJECT
public:
    explicit DownloadManager(QObject *parent = nullptr);
    void appendRawFic(const QString& urlFirstChap);
    void appendFic(FicDownloadData ficDlData);
    void appendChapter(const QString& url);
    void appendChapters(const QStringList& urls);

signals:
    void finished();

private slots:
    void startNextDownload();
    void initialDownloadFinished();
    void downloadFinished();
    void downloadReadyRead();

public:
    QQueue<FicDownloadData> fanficVirtQueue;
    QQueue<QUrl>            chapterQueue;
    QNetworkAccessManager   manager;

    QNetworkReply           *currentReply = nullptr;
    QNetworkReply           *initialDownload = nullptr;
    QFile                   output;
};

#endif // DOWNLOADMANAGER_H
