import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { useEffect, useState } from 'react';

import Board from './Board';
import Data from './Data';
import { SecondaryButton } from './Button'

export default function App() {
  const emptyCombinations = Array(9).fill('W');
  const [finalCombinations, setFinalCombinations] = useState([...emptyCombinations]);

  useEffect(() => {
    randomizeHandler()
  }, [],)

  function randomizeHandler() {
    const combinations = Data();
    const combinationNumber = Math.floor(Math.random() * combinations.length);
    setFinalCombinations(combinations[combinationNumber]);
  }

  return (
    <View style={styles.container}>
      <StatusBar style="dark" />
      <Text style={styles.text}>Kasane Iro Theme Card</Text>
      <Board finalCombinations={finalCombinations} />
      <View style={styles.buttonContainer}>
        <SecondaryButton style={styles.button} onPress={randomizeHandler}>
          Randomize
        </SecondaryButton>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#111A2D',
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontSize: 42,
    textAlign: 'center',
    padding: 10,
    marginTop: 100,
  },
  buttonContainer: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  button: {
    alignSelf: 'center',
    width: 150,
    marginHorizontal: 20,
  },
});
