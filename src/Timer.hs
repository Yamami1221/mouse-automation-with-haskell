module Timer
    ( runTimer
    ) where

import Control.Concurrent (writeChan, Chan, threadDelay)

type Seconds = Int

runTimer :: Chan Bool -> Seconds -> IO ()
runTimer chan 0 = writeChan chan False
runTimer chan seconds = do
    threadDelay 1000000
    runTimer chan (seconds - 1)
