#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_actionQuit_triggered()
{
    if (QMessageBox::question(this, tr("Quit"), tr("Exit the application?"), QMessageBox::Yes | QMessageBox::No) == QMessageBox::Yes) {
            qApp->closeAllWindows();
        }
}
