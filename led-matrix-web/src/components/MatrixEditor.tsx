import { useState, useCallback } from 'react'
import {
  Box,
  SimpleGrid,
  Button,
  VStack,
  HStack,
  Select,
  useToast,
} from '@chakra-ui/react'

type LED = {
  on: boolean
  color: string
}

const MATRIX_SIZE = 8
const DEFAULT_COLOR = '#FFFFFF'

export const MatrixEditor = () => {
  const [matrix, setMatrix] = useState<LED[][]>(() =>
    Array(MATRIX_SIZE).fill(null).map(() =>
      Array(MATRIX_SIZE).fill(null).map(() => ({ on: false, color: DEFAULT_COLOR }))
    )
  )

  const [selectedColor, setSelectedColor] = useState(DEFAULT_COLOR)
  const toast = useToast()

  const toggleLED = useCallback((row: number, col: number) => {
    setMatrix(prev => {
      const newMatrix = [...prev]
      newMatrix[row] = [...prev[row]]
      const currentLED = prev[row][col]
      newMatrix[row][col] = {
        on: !currentLED.on,
        color: !currentLED.on ? selectedColor : DEFAULT_COLOR
      }
      return newMatrix
    })
  }, [selectedColor])

  const handleExport = useCallback(() => {
    const data = {
      matrix,
      timestamp: new Date().toISOString(),
      size: MATRIX_SIZE
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `led-matrix-${data.timestamp}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    toast({
      title: 'Matrix exported successfully',
      status: 'success',
      duration: 3000,
      isClosable: true,
    })
  }, [matrix, toast])

  const resetMatrix = useCallback(() => {
    setMatrix(Array(MATRIX_SIZE).fill(null).map(() =>
      Array(MATRIX_SIZE).fill(null).map(() => ({ on: false, color: DEFAULT_COLOR }))
    ))
  }, [])

  return (
    <VStack spacing={8} align="center">
      <Box
        borderWidth={2}
        borderColor="gray.200"
        borderRadius="lg"
        p={4}
        bg="white"
        shadow="md"
      >
        <SimpleGrid columns={MATRIX_SIZE} spacing={2}>
          {matrix.map((row, rowIndex) =>
            row.map((led, colIndex) => (
              <Box
                key={`${rowIndex}-${colIndex}`}
                w="40px"
                h="40px"
                bg={led.on ? led.color : 'gray.800'}
                borderRadius="md"
                cursor="pointer"
                onClick={() => toggleLED(rowIndex, colIndex)}
                transition="all 0.2s"
                _hover={{
                  transform: 'scale(1.1)',
                }}
              />
            ))
          )}
        </SimpleGrid>
      </Box>

      <HStack spacing={4}>
        <Select
          value={selectedColor}
          onChange={(e) => setSelectedColor(e.target.value)}
          w="200px"
        >
          <option value="#FFFFFF">White</option>
          <option value="#FF0000">Red</option>
          <option value="#00FF00">Green</option>
          <option value="#0000FF">Blue</option>
          <option value="#FFFF00">Yellow</option>
          <option value="#FF8C00">Orange</option>
          <option value="#FF00FF">Pink</option>
        </Select>
        <Button colorScheme="blue" onClick={handleExport}>
          Export
        </Button>
        <Button colorScheme="red" variant="outline" onClick={resetMatrix}>
          Reset
        </Button>
      </HStack>
    </VStack>
  )
} 