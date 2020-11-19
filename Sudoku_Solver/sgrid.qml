import QtQuick 2.0

Rectangle {
    id: outerFrame
    width: 428; height: 428; color: "black"
    enabled: false

    Grid {
        id: outerGrid
        x: 5
        y: 5
        width: 418
        height: 418
        rows: 3; columns: 3; spacing: 11

        Repeater { id: innerRepeater; enabled: false; model: 9
            Grid {
                id: innerGrid
                x: 5; y: 5
                width: 133
                height: 133
                rows: 3; columns: 3; spacing: 5

                Repeater { id: cellRepeater; enabled: false; model: 9
                    Rectangle { width: 40; height: 40
                                       color: "white"

                                       Text { id: index; text: qsTr("1")
                                           font.pointSize: 12
                                              anchors.centerIn: parent } }
                }
            }

        }
    }


}
