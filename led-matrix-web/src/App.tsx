import { ChakraProvider, Box, VStack, Heading, useColorModeValue } from '@chakra-ui/react'
import { MatrixEditor } from './components/MatrixEditor'

function App() {
  return (
    <ChakraProvider>
      <Box minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')} p={8}>
        <VStack spacing={8}>
          <Heading>LED Matrix Art Maker</Heading>
          <MatrixEditor />
        </VStack>
      </Box>
    </ChakraProvider>
  )
}

export default App
