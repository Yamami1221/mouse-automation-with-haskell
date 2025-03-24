{-# LANGUAGE InstanceSigs #-}
module EitherTransformer
    ( EitherT(..)
    ) where

import Control.Monad.Trans.Class (MonadTrans (lift))

newtype EitherT a m b = EitherT {runEitherT :: m (Either a b)}

instance (Functor m) => Functor (EitherT a m) where
  fmap :: (b -> c) -> EitherT a m b -> EitherT a m c
  fmap f = EitherT . fmap (fmap f) . runEitherT

instance (Monad m) => Applicative (EitherT a m) where
  pure ::b -> EitherT a m b
  pure = EitherT . pure . Right

  (<*>) ::EitherT a m (b -> c) -> EitherT a m b -> EitherT a m c
  EitherT mf <*> EitherT ma = EitherT $ do
    f <- mf
    a <- ma
    return $ f <*> a

instance (Monad m) => Monad (EitherT a m) where
  (>>=) :: EitherT a m b -> (b -> EitherT a m c) -> EitherT a m c
  (EitherT ma) >>= f = EitherT $ ma >>= either (return . Left) (runEitherT . f)

instance MonadTrans (EitherT a) where
  lift :: (Monad m) => m b -> EitherT a m b
  lift = EitherT . fmap Right