import { StyleSheet, View } from 'react-native'

export default function Cell({color}) {
    const backgroundColor = {
        'R': '#fd9cca',
        'B': '#87d9ff',
        'Y': '#f1e376',
        'P': '#9d86ce',
        'O': '#f6956a',
        'G': '#89cb9b',
        'W': '#eae8ed'
    }
    return (
        <View style={[styles.cell, {backgroundColor: backgroundColor[color]}]} />
    )
}
const styles = StyleSheet.create({
    cell: {
        height: 100,
        width: 100,
        margin: 2,
    },
})