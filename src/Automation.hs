module Automation
    ( runAutomation
    ) where

import System.Win32.Automation.Input (sendInput, INPUT(..))
import System.Win32.Automation.Input.Mouse (mOUSEEVENTF_LEFTDOWN, mOUSEEVENTF_LEFTUP, MOUSEINPUT(..))
import Control.Concurrent (forkIO, threadDelay, killThread)
import Control.Concurrent.Chan (newChan, writeChan, readChan, Chan)
import Control.Monad.Extra (whileM)
import Control.Monad (forever)
import Graphics.Win32.Key (getAsyncKeyState, vK_ESCAPE)
import Timer (runTimer)
import Graphics.Win32 (setCursorPos)
import Data.Bifunctor (bimap)
import EitherTransformer (EitherT(..))
import Control.Monad.Trans.Class (MonadTrans (lift))
import Text.Read (readMaybe)

data Mode = Click | Move

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

-- loop :: IO () -> IO ()
-- loop = loopWithDelay 100

loopWithDelay :: Int -> IO () -> IO ()
loopWithDelay delay action = do
    _ <- forever $ do
        threadDelay delay
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

    modeAndSec <- runEitherT setup
    timeout <- readTimeout
    actionT <- case modeAndSec of
        Left err -> error err
        Right (Click, second) -> forkIO $ loopWithDelay second mouseClick
        Right (Move, second) -> forkIO $ loopWithDelay second $ mouseMultiMove [(269, 1064), (943, 598), (725, 717), (1104, 809), (972, 728), (971, 940), (701, 992), (1800, 24)] (500 * 1000)
    listenerT <- forkIO $ listenKeyUntil chan $ fromIntegral vK_ESCAPE
    timerT <- case timeout of
        Left err -> error err
        Right s -> forkIO $ runTimer chan s

    whileM $ do
        threadDelay 100
        readChan chan

    killThread listenerT
    killThread actionT
    killThread timerT
    return ()

setup :: EitherT String IO (Mode, Int)
setup = do
    mode <- selectMode
    second <- readDelay
    EitherT . return $ Right (mode, second)

selectMode :: EitherT String IO Mode
selectMode = do
    lift $ putStrLn "Select mode:"
    lift $ putStrLn "1. Click"
    lift $ putStrLn "2. Move"
    selection <- lift getLine
    EitherT $ case selection of
        "1" -> return $ Right Click
        "2" -> return $ Right Move
        _ -> return $ Left "Invalid mode"

readDelay :: EitherT String IO Int
readDelay = do
    lift $ putStrLn "Enter microsecond to delay:"
    second <- lift getLine
    EitherT $ case read second of
        Just s -> return $ Right s
        Nothing -> return $ Left "Invalid second"

readTimeout :: IO (Either String Int)
readTimeout = do
    putStrLn "Enter timeout in second:"
    second <- getLine
    return $ case readMaybe second of
        Just s -> Right s
        Nothing -> Left "Invalid second"