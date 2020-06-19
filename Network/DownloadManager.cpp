#include "DownloadManager.h"

#include <iostream>

DownloadManager::DownloadManager(QObject *parent)
    : QObject(parent)
{

}

void DownloadManager::appendRawFic(const QString& urlFirstChap)
{
    QNetworkRequest request(urlFirstChap);
    initialDownload = manager.get(request);

    connect(initialDownload, &QNetworkReply::finished, this, &DownloadManager::initialDownloadFinished);
}

void DownloadManager::appendChapter(const QString& url)
{
    std::cout << "Added " << url.toStdString() << std::endl;
    chapterQueue.enqueue(QUrl(url));

}


void DownloadManager::startNextDownload()
{
    if (chapterQueue.isEmpty()) {
        std::cout << "All Downloads finished" << std::endl;
    }

    QUrl chapURL = chapterQueue.dequeue();
    std::string fname = Utils::getFilenameChapter("JPT", chapURL.toString().toStdString());
    QString fileName = QString(fname.c_str());

    output.setFileName(fileName);
    if (!output.open(QIODevice::WriteOnly)) {
        std::cout << "ERROR OPENING: " << fname << std::endl;

        startNextDownload();
        return;
    }

    QNetworkRequest request(chapURL);
    currentReply = manager.get(request);

    connect(currentReply, &QNetworkReply::finished, this, &DownloadManager::downloadFinished);
    connect(currentReply, &QNetworkReply::readyRead, this, &DownloadManager::downloadReadyRead);
}

void DownloadManager::initialDownloadFinished()
{
    QByteArray chapOneArr = initialDownload->readAll();
    const char *contents = chapOneArr.constData();

    printf("DL: %s\n", contents);

    initialDownload->deleteLater();
}

void DownloadManager::downloadFinished()
{
    output.close();

    if (currentReply->error()) {
        std::cout << "Download failed\n";
        output.remove();
    } else {
        // forgo checking for redirect
        std::cout << "Downloaded\n";
    }

    currentReply->deleteLater();
    startNextDownload();
}

void DownloadManager::downloadReadyRead()
{
    output.write(currentReply->readAll());
}

