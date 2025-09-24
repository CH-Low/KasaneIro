import { StyleSheet, View } from 'react-native'
import Cell from './Cell'

export default function Board({finalCombinations}) {
    return (
        <View style={styles.container}>
            {[...Array(3)].map((x, column) =>
                <View key={'row_' + column} style={styles.row}>
                    {[...Array(3)].map((y, row) =>
                        <Cell key={`${row * 3 + column}`} color={finalCombinations[row * 3 + column]}/>
                    )}
                </View>
            )}
        </View>
    )
}
const styles = StyleSheet.create({
    container: {
        paddingVertical: 10,
        paddingHorizontal: 10,
        borderRadius: 20,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#eae8ed',
        marginBottom: 20
    },
    row: {
        backgroundColor: '#eae8ed',
    },
})