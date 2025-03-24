module Automation
    ( runAutomation
    ) where

import System.Win32.Automation.Input (sendInput, INPUT(..))
import System.Win32.Automation.Input.Mouse (mOUSEEVENTF_LEFTDOWN, mOUSEEVENTF_LEFTUP, MOUSEINPUT(..))
import Control.Concurrent (forkIO, newChan, writeChan, readChan, Chan, threadDelay, killThread)
import Control.Monad.Extra (whileM)
import Control.Monad (forever)
import Graphics.Win32.Key (getAsyncKeyState, vK_ESCAPE)
import Timer (runTimer)
import Graphics.Win32 (setCursorPos)
import Data.Bifunctor (bimap)

type XPos = Int
type YPos = Int

mouseMove :: (XPos, YPos) -> IO ()
mouseMove = setCursorPos . bimap fromIntegral fromIntegral

mouseMultiMove :: [(XPos, YPos)] -> Int -> IO ()
mouseMultiMove [] _ = return ()
mouseMultiMove (pos:rest) delay = do
    mouseMove pos
    threadDelay delay
    mouseMultiMove rest delay

mouseClick :: IO ()
mouseClick = do
    _ <- sendInput [Mouse $ MOUSEINPUT 0 0 0 mOUSEEVENTF_LEFTDOWN 0 0, Mouse $ MOUSEINPUT 0 0 0 mOUSEEVENTF_LEFTUP 0 0]
    return ()

loop :: IO () -> IO ()
loop action = do
    _ <- forever $ do
        threadDelay 100
        action
    return ()

listenKeyUntil :: Chan Bool -> Int -> IO ()
listenKeyUntil chan key = do
    whileM $ do
        threadDelay 100
        status <- getAsyncKeyState key
        return (status == 0)
    writeChan chan False
    return ()

runAutomation :: IO ()
runAutomation = do
    chan <- newChan :: IO (Chan Bool)
    writeChan chan True
    listenerT <- forkIO $ listenKeyUntil chan $ fromIntegral vK_ESCAPE
    actionT <- forkIO $ loop mouseClick
    -- actionT <- forkIO $ loop $ mouseMultiMove [(269, 1064), (943, 598), (725, 717), (1104, 809), (972, 728), (971, 940), (701, 992), (1800, 24)] (500 * 1000)
    timerT <- forkIO $ runTimer chan 10
    whileM $ do
        threadDelay 100
        readChan chan
    killThread listenerT
    killThread actionT
    killThread timerT
    return ()